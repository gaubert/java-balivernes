""" 
    Copyright 2008 CTBTO Organisation
    
    module: generate_noble_gaz_arr
"""

import getopt, sys
import datetime
import os
import logging
import logging.handlers
import StringIO
import traceback

import ctbto.common.xml_utils
import ctbto.common.time_utils
import ctbto.common.utils
from org.ctbto.conf    import Conf
from ctbto.db          import DatabaseConnector,DBDataFetcher
from ctbto.renderers   import SaunaRenderer
from ctbto.transformer import XML2HTMLRenderer

NAME        = "generate_arr"
VERSION     = "1.0"
DATE_FORMAT = "%Y-%m-%d"

def usage():
    
    usage_string = """
Usage: generate_arr [options] 

  Mandatory Options:
  --sids     (-s)   Retrieve the data and create the ARR of the following sample ids.
                    If --sids and --from or --end are used only the information provided with --sids will be used.
  or
  
  --from     (-f)   Get all the sample ids corresponding to the from date until the end date  (default=today).
                    The date is in the YYYY-MM-DD form (ex: 2008-08-22)
  --end      (-e)   Get all the sample ids created during the from and end period             (default=yesterday).
                    The date is in the YYYY-MM-DD form (ex: 2008-08-22)
  --stations (-t)   Get all the sample ids belonging to the passed stations code              (default=all SAUNA stations)
                    ex: --stations USX74,CAL05
             

  Extra Options:
  --dir           (-d)       Destination directory where the data will be written.            (default=/tmp)
                             The SAMPML files will be added under DIR/samples and the ARR
                             under DIR/ARR. 
                             The directories will be created if not present
  --conf_dir      (-c)       directory containing a configuration file rnpicker.config        (default=$RNPICKER_CONF_DIR)  
  
  --vvv           (-3)       Increase verbosity ot level 3 in order to have all the errors
                             in the stdout  


  Help Options:
   --help     Show this usage information.

  Examples:
  >./generate_arr --sids 211384,248969 --dir ./results 
  
  Get the SAMPML and ARR files for the sample ids 211384 and 248969 and store them in ./results.
  
  >./generate_arr --stations USX74,CAL05 --dir ./results 
  
  Get the SAMPML and ARR files for the samples belonging to the stations USX75 and CAL05
  from yesterday to today.
  
  >./generate_arr --from 2008-12-02 --end 2009-01-15 --dir ./results --conf_dir ../conf
  
  Get the SAMPML and ARR files for the samples belonging to all the SAUNA stations for the passed
  period. The configuration file rnpicker.config fron ../conf will be used to get the configuration
  information.
 
  """
       
    print(usage_string)

import ctbto.tests
def get_tests_dir_path():
    """
            get the ctbto.tests path depending on where it is defined
        
            Args:
               None
               
            Returns:
               return the path as a string
        
            Raises:
               exception
    """    
    fmod_path = ctbto.tests.__path__
        
    test_dir = "%s/conf_tests"%fmod_path[0]
        
    return test_dir

def get_exception_traceback():
    """
            return the exception traceback (stack info and so on) in a string
        
            Args:
               None
               
            Returns:
               return a string that contains the exception traceback
        
            Raises:
               
    """
    f = StringIO.StringIO()
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info() #IGNORE:W0702
    traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,file=f)
    return f.getvalue()

def parse_arguments(a_args):
    """
            return the checksum of the calibration coeffs. This is done to create a unique id for the different calibration types.
        
            Args:
               a_args: list of arguments to parse. 
               
            Returns:
               return a dict containing all the parsed arguments
        
            Raises:
               exception
    """
    
    result = {}
    
    # add default
    result['dir'] = "/tmp/"
    result['verbose'] = 1
    
    try:
        (opts,_) = getopt.getopt(a_args, "ht:s:f:e:d:c:v3", ["help","stations=","sids=","from=","end=","dir=","conf_dir=","version","vvv"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            print("%s v %s"%(NAME,VERSION))
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--sids"):
            # if there is a comma try to build a list
            if a.find(',') != -1:
                sids = a.split(',')
                # insure that each sid only contains digits
                for s in sids:
                    if not s.isdigit():
                        raise ParsingError("Error passed sid %s (with --sids or -s) is not a number"%(s)) 
                result['sids'] = sids   
            elif a.isdigit():
                result['sids'] = [a]                
            else:
                raise ParsingError("Error passed sid %s (with --sids or -s) is not a number"%(a))
        elif o in ("-t", "--stations"):
            # if there is a comma try to build a list
            if a.find(',') != -1:
                stations = a.split(',')
                
                l = []
                for elem in stations:
                    l.append("\'%s\'"%(elem))
                
                # insure that each sid only contains digits    
                result['stations'] = l  
            else:
                result['stations'] = ["\'%s\'"%(a)]                
        elif o in ("-d", "--dir"):
            # try to make the dir if necessary
            ctbto.common.utils.makedirs(a)
            result['dir'] = a   
        elif o in ("-3","--vvv"):
            result['verbose'] = 3 
        elif o in ("-f", "--from"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a,DATE_FORMAT)
                result['from'] = a
            except:
                raise ParsingError("Invalid --from or -f date %s"%(a))
        elif o in ("-e", "--end"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a,DATE_FORMAT)
                result['end'] = a
            except:
                raise ParsingError("Invalid --from or -f date %s"%(a))
        elif o in ("-c", "--conf_dir"):
            try:
                #check that it is a dir
                if not os.path.isdir(a):
                    raise ParsingError("%s --conf_dir or -d is not a directory")
                result['conf_dir'] = a
            except:
                raise ParsingError("Invalid --conf_dir or -d %s"%(a))
        else:
            raise ParsingError("Unknown option %s = %s"%(o,a))
    
    return result

#SQL_GETSAUNASAMPLEIDS = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (522, 684) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"

SQL_GETSAUNASAMPLEIDS = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (%s) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"

SQL_GETALLSAUNASTATIONCODES = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where type=\'SAUNA\'"

SQL_GETALLSAUNASTATIONIDSFROMCODES = "select STATION_ID from RMSMAN.GARDS_STATIONS where station_code in (%s)"

#SQL_GETSAUNASAMPLEIDS2  = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in () RMSMAN.GARDS_STATIONS"

class ParsingError(Exception):
    """The only exception where a logger as not yet been set as it depends on the conf"""

    def __init__(self,aMsg):
        super(ParsingError,self).__init__()
        self.message = aMsg
        
class ConfAccessError(Exception):
    """The only exception where a logger as not yet been set as it depends on the conf"""

    def __init__(self,aMsg):
        super(ConfAccessError,self).__init__()
        self.message = aMsg

class Runner(object):
    """ Class for fetching and producing the ARR """
    
    # Class members
    c_log = logging.getLogger("Runner")
    c_log.setLevel(logging.INFO)


    def __init__(self,a_args):
        
        super(Runner,self).__init__()
          
        # create an empty shell Conf object
        self._conf = self._load_configuration(a_args)
        
        self._set_logging_configuration()
    
        # setup the prod databasse and connect to it
        self._ngDatabase        = self._conf.get("NobleGazDatabaseAccess","hostname")
        self._ngUser            = self._conf.get("NobleGazDatabaseAccess","user")
        self._ngPassword        = self._conf.get("NobleGazDatabaseAccess","password")
        self._ngActivateTimer   = self._conf.getboolean("NobleGazDatabaseAccess","activateTimer",True)
   
        # create DB connector
        self._ngMainConn = DatabaseConnector(self._ngDatabase,self._ngUser,self._ngPassword,self._ngActivateTimer)

        # setup the archive database and connect to it
        self._archiveDatabase       = self._conf.get("ArchiveDatabaseAccess","hostname")
        self._archiveUser           = self._conf.get("ArchiveDatabaseAccess","user")
        self._archivePassword       = self._conf.get("ArchiveDatabaseAccess","password")
        self._archiveActivateTimer  = self._conf.getboolean("ArchiveDatabaseAccess","activateTimer",True)
        
        # create DB connector
        self._ngArchConn = DatabaseConnector(self._archiveDatabase,self._archiveUser,self._archivePassword,self._archiveActivateTimer)
        
        #connect to the DBs
        self._ngMainConn.connect()
        self._ngArchConn.connect()
        
    def _set_logging_configuration(self):
        """
            setup the logging info.
            Set the root logger and the hanlders. 
            Read the information from the configuration file.
            Two handlers are created: one logging in a file file_handler. This one logs everything by default
            and another one logging a minimal set of info in the console. 
        
            Args:
               None 
               
            Returns:
               return a conf object
        
            Raises:
               exception
        """
        if len(logging.root.handlers) == 0:
            
            # create logger that logs in rolling file
            file_handler = logging.handlers.RotatingFileHandler(self._conf.get('Logging','fileLogging','/tmp/rnpicker.log'), "a", 5000000, 4)
            file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            
            # create logger that logs in console
            console = logging.StreamHandler()
            console_formatter = logging.Formatter("%(levelname)s - %(message)s")
            console_filter    = logging.Filter(self._conf.get('Logging','consoleFilter','Runner'))
            console.setFormatter(console_formatter)
            console.addFilter(console_filter)
        
            logging.root.addHandler(file_handler)
            logging.root.addHandler(console)
        
    def _load_configuration(self,a_args):
        """
            try to load the configuration from the config file.
            priority rules: if --conf_dir is set, try to read a dir/rnpicker.config. Otherwise look for RNPICKER_CONF_DIR env var
        
            Args:
               None 
               
            Returns:
               return a conf object
        
            Raises:
               exception
        """
        
        #read from command_line
        dir = a_args.get('conf_dir',None)
        
        #try to read from env
        if dir == None:
            dir = os.environ.get('RNPICKER_CONF_DIR',None)
        else:
            #always force the ENV Variable
            os.environ['RNPICKER_CONF_DIR'] = dir
        
        if dir is None:
            raise ConfAccessError('The conf dir needs to be set from the command line or using the env variable RNPICKER_CONF_DIR')
        
        if os.path.isdir(dir):
            os.environ[Conf.ENVNAME] = '%s/%s'%(dir,'rnpicker.config')
            
            return Conf.get_instance()
        else:
            raise ConfAccessError('The conf dir %s set with the env variable RNPICKER_CONF_DIR is not a dir'%(dir))
        
    def _get_list_of_sauna_sampleIDs(self,stations='',beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='1000000'):
        
        l = ','.join(map(str,stations)) #IGNORE:W0141
        
        result = self._ngMainConn.execute(SQL_GETSAUNASAMPLEIDS%(l,beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        Runner.c_log.info("Found %d sampleIDs: %s\n"%(len(sampleIDs),sampleIDs))
       
        return sampleIDs
    
    def _get_stations_ids(self,a_station_codes):
        
        result = self._ngMainConn.execute(SQL_GETALLSAUNASTATIONIDSFROMCODES%(','.join(a_station_codes)))
        
        sta_ids    = []
        
        rows   = result.fetchall()
        
        for row in rows:
            sta_ids.append(row[0])
            
        return sta_ids
    
    def _get_all_stations(self):
        
        result = self._ngMainConn.execute(SQL_GETALLSAUNASTATIONCODES)
        
        sta_codes  = []
        sta_ids    = []
        
        rows   = result.fetchall()
        
        for row in rows:
            sta_codes.append(row[0])
            sta_ids.append(row[1])
            
        Runner.c_log.info("Found the following SAUNA stations: %s\n"%(sta_codes))
        
        return sta_ids
    
    def _create_directories(self,dir):
        
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s/samples'%(dir))
        
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s/ARR'%(dir))

    def execute(self,a_args):
    
        if a_args == None or a_args == {}:
            return
        
        # default request => do not retrieve PREL but all the rest
        request="spectrum=CURR/DETBK/GASBK/QC, analysis=CURR"
        
        # check if we have some sids or we get it from some dates
        
        if 'sids' in a_args:
            sids    = a_args['sids']
        elif 'from' in a_args or 'end' in a_args or 'stations' in a_args:
            begin    = a_args.get('from',ctbto.common.time_utils.getYesterday())
            end      = a_args.get('end',ctbto.common.time_utils.getToday())
            stations = a_args.get('stations',None)
            if stations != None:
                stations = self._get_stations_ids(stations)
            else:
                stations = self._get_all_stations()
            sids     = self._get_list_of_sauna_sampleIDs(stations,begin, end)
        else:
            raise Exception('need either a sid or some dates')
    
        dir = a_args['dir']
        
        self._create_directories(dir)
        
        #to_ignore = [53758,141372,141501,206975]
        to_ignore = self._conf.getlist('IgnoreSamples','noblegazSamples')
    
        for sid in sids:
            
            if sid in to_ignore:
                Runner.c_log.info("*************************************************************")
                Runner.c_log.info("Ignore the retrieval of the sample id %s as it is incomplete."%(sid))
                Runner.c_log.info("*************************************************************\n")
                #skip this iteration
                continue
    
            Runner.c_log.info("*************************************************************")
            Runner.c_log.info("Fetch data and build SAMPML data file for %s"%(sid))
            
            # fetch noble gaz or particulate
            fetcher = DBDataFetcher.getDataFetcher(self._ngMainConn,self._ngArchConn,sid)
   
            #modify remoteHost
            fetcher.setRemoteHost(self._conf.get('RemoteAccess','nobleGazRemoteHost','dls007'))
            
            fetcher.fetch(request,'GAS')
                 
            renderer = SaunaRenderer(fetcher)
   
            xmlStr = renderer.asXmlStr(request)
           
            path = "%s/samples/sampml-full-%s.xml"%(dir,sid)
   
            Runner.c_log.info("Save SAMPML data in %s"%(path))
            
            ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
            
            Runner.c_log.info("Create ARR from SAMPML data file for %s"%(sid))
           
            r = XML2HTMLRenderer('%s/%s'%(get_tests_dir_path(),'templates'),'ArrHtml.html')
    
            result = r.render(path)
            
            path = "%s/ARR/ARR-%s.html"%(dir,sid)
            
            Runner.c_log.info("save file in %s"%(path))
            
            ctbto.common.utils.printInFile(result,path)
            
            Runner.c_log.info("*************************************************************\n")
  
def run():
    parsed_args = {}
    
    try:
        parsed_args = parse_arguments(sys.argv[1:])
         
        runner = Runner(parsed_args)
        
        runner.execute(parsed_args) 
    except ParsingError, e:
        # Not Runner set print
        print "Error: %s"%(e.message) 
        usage() 
        sys.exit(2)
    except ConfAccessError, e:
        # Not Runner set print
        print "Error: %s"%(e.message) 
        usage() 
        sys.exit(2)
    except Exception, e: #IGNORE:W0703,W0702
        Runner.c_log.error("Error: %s. For more information see the log file."%(e))
        if parsed_args.get('verbose',1) == 3:
            a_logger = Runner.c_log.error
        else:
            a_logger = Runner.c_log.debug
        a_logger("Traceback: %s."%(get_exception_traceback()))
        usage()
        sys.exit(3)
    
    sys.exit(0)
          
if __name__ == "__main__":
    
    run()
    #usage()
