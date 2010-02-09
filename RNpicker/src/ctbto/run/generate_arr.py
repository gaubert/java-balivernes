
"""
    :Summary: generate noble gaz arr
    :Creation date: 2008-01-15
    :Version: 1.0
    :Authors: guillaume.aubert@ctbto.org
    :Copyright: 2008 CTBTO Organisation

"""

import getopt, sys
import datetime
import os
import StringIO
import traceback

import ctbto.common.time_utils
import ctbto.common.utils
import ctbto.common.xml_utils
from ctbto.common.logging_utils import LoggerFactory
from org.ctbto.conf    import Conf
from ctbto.db          import DatabaseConnector, DBDataFetcher
from ctbto.renderers   import BaseRenderer
from ctbto.transformer import SAUNAXML2HTMLRenderer, SPALAXXML2HTMLRenderer

NAME        = "generate_arr"
VERSION     = "1.0"
DATE_FORMAT = "%Y-%m-%d"

def usage():
    """
     Usage message
    """
    
    usage_string = """
Usage: generate_arr [options] 

  Mandatory Options:
  --sids           (-i)   Retrieve the data and create the ARR of the following sample ids.
                          If --sids and --from or --end are used only the information provided 
                          with --sids will be used.
  or
  
  --from           (-f)   Get all the sample ids corresponding to the from date (00H00m00s) until the end date (00H00m00s). (default=today).
                          The date is in the YYYY-MM-DD form (ex: 2008-08-22).
  --end            (-e)   Get all the sample ids created during the from and end period.            (default=yesterday).
                          The date is in the YYYY-MM-DD form (ex: 2008-08-22).
  or
  
  --stations       (-t)   Get all the sample ids belonging to the passed stations code.             (default=all SAUNA stations)
                          ex: --stations USX74,CAL05.
             

  Extra Options:
  --dir             (-d)  Destination directory where the data will be written.                     (default=/tmp/samples)
                          The SAMPML files will be added under DIR/samples and the ARR
                          under DIR/ARR. 
                          The directories will be created if not present.
                          
  --conf_dir        (-c)  Directory containing a configuration file rnpicker.config.                (default=$RNPICKER_CONF_DIR)  
  
  --vvv             (-3)  Increase verbosity to level 3 in order to have all the errors
                          in the stdout.  
  
  Advanced Options:
  --clean_cache         (-l)  Clean the caching area as defined in the configuration file.
  
  --clean_local_spectra (-o)  Clean the directory containing the spectra cached locally
                              as defined in the configuration file.
  
  --automatic_tests     (-a)  Run the automatic tests and exit.


  Help Options:
   --help     Show this usage information.

  Examples:
  >./generate_arr --sids 211384,248969 --dir ./results 
  
  Get the SAMPML and ARR files for the sample ids 211384 and 248969 and store them in ./results.
  
  >./generate_arr --stations USX74,CAL05 --dir ./results 
  
  Get the SAMPML and ARR files for the samples belonging to the stations USX75 and CAL05
  from yesterday to today.
  
  >./generate_arr --from 2009-01-15 --stations CNX22,USX75
  
  Get the SAMPML and ARR files for the samples belonging to the stations CNX22 and USX75
  and produced from the 15 of Jan 2009 until today.
  
  >./generate_arr --from 2008-12-02 --end 2009-01-15 --dir ./results --conf_dir ../conf
  
  Get the SAMPML and ARR files for the samples belonging to all the SAUNA stations for the passed
  period. The configuration file rnpicker.config under ../conf will be used to get the configuration
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
        
    test_dir = "%s/conf_tests" % fmod_path[0]
        
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
    the_file = StringIO.StringIO()
    exception_type, exception_value, exception_traceback = sys.exc_info() #IGNORE:W0702
    traceback.print_exception(exception_type, exception_value, exception_traceback, file = the_file)
    return the_file.getvalue()

def reassociate_arguments(a_args):
    """
        reassociate arguments passed in the program arguments when they are spearated by a space.
        a, b , c will become 'a, b ,c'
    """
    the_list = len(a_args)
    
    if the_list <= 1:
        return a_args
    else:
        res = []
        _reassoc_arguments(a_args[0], a_args[1:], res)
        return res

def _reassoc_arguments(head, tail, res, memo=''): 
    """
            private function used to recurse in reassociate_arguments
    """
    # stop condition, no more fuel
    if len(tail) == 0:
        # if command separate
        if head.startswith('-'):
            res.extend([memo, head])
            return
        else:
            res.append(memo + head)
            return
    
    if head.endswith(',') or head.startswith(','):
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo+head)
    elif head.startswith('-'):
        # we do have a command so separate it from the rest
        if len(memo) > 0:
            res.append(memo)
            
        res.append(head)
        
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, '')
    else:  
        # it is not a command 
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo+head) 
            
    

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
    
    # add defaults
    result['dir']                   = "/tmp/samples"
    result['verbose']               = 1
    result['clean_cache']           = False
    result['automatic_tests']       = False
    result['clean_local_spectra']   = False
    result['station_types']         = ['SAUNA', 'SPALAX']
    result['always_recreate_files'] = True
    
    try:
        reassoc_args = reassociate_arguments(a_args)
        (opts, _) = getopt.gnu_getopt(reassoc_args, "ht:i:s:f:e:d:c:v3lao", ["help", "clean_local_spectra", \
                                                                             "clean_cache", "stations=", \
                                                                             "sids=", "from=", "end=", \
                                                                             "dir=", "conf_dir=", "version", \
                                                                             "vvv", "automatic_tests"])
    except Exception, err: #IGNORE:W0703
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
        elif o in ("-i", "--sids"):
            # if there is a comma try to build a list
            if a.find(',') != -1:
                sids = a.split(',')
                # insure that each sid only contains digits
                good_sids = []
                for s in sids:
                    s=s.strip()
                    if len(s) == 0:
                        continue
                    if not s.isdigit():
                        raise ParsingError("Error passed sid [%s] (with --sids or -s) is not a number"%(s)) 
                    else:
                        good_sids.append(s)
                result['sids'] = good_sids   
            elif a.isdigit():
                result['sids'] = [a]                
            else:
                raise ParsingError("Error passed sid %s (with --sids or -s) is not a number"%(a))
             
        elif o in ("-s", "--stations"):
            # if there is a comma try to build a list
            if a.find(',') != -1:
                stations = a.split(',')
                
                t_list = []
                for elem in stations:
                    t_list.append("\'%s\'" % (elem.strip()))
                
                result['stations'] = t_list  
            else:
                result['stations'] = ["\'%s\'" % (a.strip())]                
        elif o in ("-d", "--dir"):
            # try to make the dir if necessary
            ctbto.common.utils.makedirs(a)
            result['dir'] = a   
        elif o in ("-3","--vvv"):
            result['verbose'] = 3 
        elif o in ("-f", "--from"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a, DATE_FORMAT)
                result['from'] = a
            except:
                raise ParsingError("Invalid --from or -f date %s"%(a))
        elif o in ("-e", "--end"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a, DATE_FORMAT)
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
        elif o in ("-a", "--automatic_tests"):
            try:
                result['automatic_tests'] = True
            except:
                raise ParsingError("Invalid --automatic_tests or -a %s"%(a))
        elif o in ("-l", "--clean_cache"):
            try:
                result['clean_cache'] = True
            except:
                raise ParsingError("Invalid --conf_dir or -d %s"%(a))
        elif o in ("-o", "--clean_local_spectra"):
            try:
                result['clean_local_spectra'] = True
            except:
                raise ParsingError("Invalid --clean_local_spectra or -o %s"%(a))
        else:
            raise ParsingError("Unknown option %s = %s"%(o, a))
    
    return result


SQL_GETSAMPLEIDS                   = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (%s) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"

SQL_GETALLSAUNASTATIONCODES        = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where type='SAUNA' or type='ARIX-4'"

SQL_GETALLSPALAXSTATIONCODES       = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where type='SPALAX'"

SQL_GETALLSTATIONIDSFROMCODES      = "select STATION_ID from RMSMAN.GARDS_STATIONS where station_code in (%s)"

class CLIError(Exception):
    """ Base class exception """
    pass

class ParsingError(CLIError):
    """Error when the command line is parsed"""

    def __init__(self, a_error_msg):
        super(ParsingError, self).__init__()
        self._error_message = a_error_msg
        
    def get_message_error(self):
        """ return error message """
        return self._error_message
        
class ConfAccessError(CLIError):
    """The only exception where a logger as not yet been set as it depends on the conf"""

    def __init__(self, a_error_msg):
        super(ConfAccessError, self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        """ return error message """
        return self._error_message

class LoggingSetupError(CLIError):
    """Error when the logger cannot be setuped"""

    def __init__(self, a_error_msg):
        super(LoggingSetupError, self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        """ return error message """
        return self._error_message

class Runner(object):
    """ Class for fetching and producing the ARR """
    
    def __init__(self, a_args):
        
        super(Runner, self).__init__()
          
        # create an empty shell Conf object
        self._conf     = Conf.get_instance()
        
        self._log = LoggerFactory.get_logger("Runner")
        
        # setup the prod database and connect to it
        self._ngDatabase        = self._conf.get("NobleGazDatabaseAccess", "hostname")
        self._ngUser            = self._conf.get("NobleGazDatabaseAccess", "user")
        self._ngPassword        = self._conf.get("NobleGazDatabaseAccess", "password")
        self._ngActivateTimer   = self._conf.getboolean("NobleGazDatabaseAccess", "activateTimer", True)
   
        # create DB connector
        self._ngMainConn = DatabaseConnector(self._ngDatabase, self._ngUser, self._ngPassword, self._ngActivateTimer)

        # setup the archive database and connect to it
        self._ParticulateArchiveDatabaseAccess       = self._conf.get("ParticulateArchiveDatabaseAccess", "hostname")
        self._archiveUser           = self._conf.get("ParticulateArchiveDatabaseAccess", "user")
        self._archivePassword       = self._conf.get("ParticulateArchiveDatabaseAccess", "password")
        self._archiveActivateTimer  = self._conf.getboolean("ParticulateArchiveDatabaseAccess", "activateTimer", True)
        
        # create DB connector
        self._ngArchConn = DatabaseConnector(self._ParticulateArchiveDatabaseAccess, self._archiveUser, \
                                             self._archivePassword, self._archiveActivateTimer)
        #connect to the DBs
        self._ngMainConn.connect()
        self._ngArchConn.connect()
    
    @classmethod
    def load_configuration(cls, a_args):
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
        dir = a_args.get('conf_dir', None)
        
        #try to read from env
        if dir == None:
            dir = os.environ.get('RNPICKER_CONF_DIR', None)
        else:
            #always force the ENV Variable
            os.environ['RNPICKER_CONF_DIR'] = dir
        
        if dir is None:
            raise ConfAccessError('The conf dir needs to be set from the command line or using the env variable RNPICKER_CONF_DIR')
        
        if os.path.isdir(dir):
            os.environ[Conf.ENVNAME] = '%s/%s' % (dir, 'rnpicker.config')
            
            return Conf.get_instance()
        else:
            raise ConfAccessError('The conf dir %s set with the env variable RNPICKER_CONF_DIR is not a dir'%(dir))
    
    @classmethod
    def log_in_file(self,aMessage):
        """ to log in the file as the ROOT logger """
        
        log = LoggerFactory.get_logger("ROOT")
        log.info(aMessage)
        
    def _get_list_of_sampleIDs(self,stations='',beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='10000000'):
        
        l = ','.join(map(str,stations)) #IGNORE:W0141
        
        result = self._ngMainConn.execute(SQL_GETSAMPLEIDS%(l,beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        self._log.info("Generate products for %d sampleIDs"%(len(sampleIDs)))
        
        self.log_in_file("list of sampleIDs to fetch: %s"%(sampleIDs))
        
        return sampleIDs
    
    def _get_stations_ids(self,a_station_codes):
        
        result = self._ngMainConn.execute(SQL_GETALLSTATIONIDSFROMCODES%(','.join(a_station_codes)))
        
        sta_ids    = []
        
        rows   = result.fetchall()
        
        for row in rows:
            sta_ids.append(row[0])
            
        # Error message is no ids found for the stations
        if len(sta_ids) == 0:
            raise Exception("Cannot find any sample ids for the stations %s. Are you sure they are valid station codes ?"%(a_station_codes))
            
        return sta_ids
    
    def _get_all_stations(self,a_stations_types):
        
        sta_ids    = []
        
        for type in a_stations_types:
        
            if   type == 'SAUNA':
                result = self._ngMainConn.execute(SQL_GETALLSAUNASTATIONCODES)
            elif type == 'SPALAX':
                result = self._ngMainConn.execute(SQL_GETALLSPALAXSTATIONCODES)
        
            sta_codes  = []
           
            rows   = result.fetchall()
        
            for row in rows:
                sta_codes.append(row[0])
                sta_ids.append(row[1])
            
            self._log.info("Found %d %s stations."%(len(sta_codes),type))
            self.log_in_file("Found the following %s stations: %s."%(type,sta_codes))
        
        return sta_ids
    
    def _create_results_directories(self,dir):
        
        # TODO need to fix that as there are some issues with the permissions checking
        #if os.path.exists(dir) and not os.access('%s/samples'%(dir),os.R_OK | os.W_OK |os.X_OK):
        #    raise Exception("Do not have the right permissions to write in result's directory %s.Please choose another result's SAMPML directory."%(dir))
        
        #if os.path.exists('%s/samples'%(dir)) and not os.access('%s/samples'%(dir),os.R_OK | os.W_OK):
        #    raise Exception("Do not have the right permissions to write in result's SAMPML directory %s.Please choose another result's SAMPML directory."%('%s/samples'%(dir)))

        #if os.path.exists('%s/ARR'%(dir)) and not os.access('%s/ARR'%(dir),os.R_OK | os.W_OK):
        #    raise Exception("Do not have the right permissions to write in result's SAMPML directory %s.Please choose another result's SAMPML directory."%('%s/ARR'%(dir)))
            
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s/samples'%(dir))
        
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s/ARR'%(dir))  
        

    def _clean_cache(self):
        """ clean the cache directory """
        
        path = self._conf.get('Caching','dir',None)
        
        self._log.info("Clean the cached data under %s"%(path))
        
        if path is not None:
            ctbto.common.utils.delete_all_under(path)
    
    def _clean_cached_spectrum(self):
        """ clean the cached spectrum """
        path = self._conf.get('RemoteAccess','localdir',None)
        
        self._log.info("Clean the cached spectra under %s"%(path))
        
        if path is not None:
            ctbto.common.utils.delete_all_under(path)

    def execute(self,a_args):
    
        if a_args == None or a_args == {}:
            raise Exception('No commands passed. See usage message.')
        
        self._log.info("*************************************************************")
        self._log.info("Configuration infos read from %s"%(self._conf.get_conf_file_path()))
        
        self._log.info("*************************************************************\n")
        
        cache_cleaned         = False
        local_spectra_cleaned = False
        
        # check if we need to clean the cache
        if a_args['clean_cache']:
            self._clean_cache()
            cache_cleaned = True
        
        if a_args['clean_local_spectra']:
            self._clean_cached_spectrum()
            local_spectra_cleaned = True
        
        # check if we can write in case the dir already exists    
        dir = a_args['dir']
        self._create_results_directories(dir)
        
        
        # default request => do not retrieve PREL but all the rest
        request="spectrum=CURR/DETBK/GASBK/QC, analysis=CURR"
        
        # check if we have some sids or we get it from some dates
        self._log.info("*************************************************************")
        
        if 'sids' in a_args:
            sids    = a_args['sids']
        elif 'from' in a_args or 'end' in a_args or 'stations' in a_args:
            begin    = a_args.get('from',ctbto.common.time_utils.getOracleDateFromISO8601(ctbto.common.time_utils.getYesterday()))
            end      = a_args.get('end',ctbto.common.time_utils.getOracleDateFromISO8601(ctbto.common.time_utils.getToday()))
            stations = a_args.get('stations',None)
            if stations != None:
                stations = self._get_stations_ids(stations)
            else:
                stations = self._get_all_stations(a_args['station_types'])
            sids     = self._get_list_of_sampleIDs(stations,begin, end)
        else:
            # if the cache has been clean then exit quietly as one action has been performed
            if cache_cleaned or local_spectra_cleaned:
                return
            else:  
                # no actions performed error
                raise Exception('need either a sid or some dates or a station name')
        
        self._log.info("Start the product generation")
        self._log.info("*************************************************************\n")
        
        to_ignore = self._conf.getlist('IgnoreSamples','noblegazSamples')
        always_recreate_files = a_args['always_recreate_files']
    
        for sid in sids:
            
            if str(sid) in to_ignore:
                self._log.info("*************************************************************")
                self._log.info("Ignore the retrieval of the sample id %s as it is incomplete."%(sid))
                self._log.info("*************************************************************\n")
                #skip this iteration
                continue
    
            self._log.info("*************************************************************")
            self._log.info("Fetch data and build SAMPML data file for %s"%(sid))
            
            # if the right flag is set and the file already exists do not recreate it
            if always_recreate_files or not os.path.exists("%s/ARR/ARR-%s.html"%(dir,sid)):
            
                # fetch noble gaz or particulate
                fetcher = DBDataFetcher.getDataFetcher(self._ngMainConn,self._ngArchConn,sid)
   
                #modify remoteHost
                fetcher.setRemoteHost(self._conf.get('RemoteAccess','nobleGazRemoteHost','dls007'))
            
                fetcher.fetch(request,'GAS')
                 
                renderer = BaseRenderer.getRenderer(fetcher)
   
                xmlStr = renderer.asXmlStr(request)
                
                station_code = fetcher.get('STATION_CODE')
           
                path = "%s/samples/sampml-full-%s-%s.xml"%(dir,station_code,sid)
   
                self._log.info("Save SAMPML data in %s"%(path))
            
                # pretty print and save in file
                ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
            
                #create ARR if possible
                self._create_arr(fetcher, dir, path, sid, station_code)
            
            else:
                self._log.info("products are already existing in %s for %s"%(dir,sid)) 
            
            self._log.info("*************************************************************\n")

    def _create_arr(self,a_fetcher,a_dir,a_path,a_sid, a_station_code):
        """ create the ARR if possible.
            ARRs will be created only for SPHDF and SPHDP
        """
        current = a_fetcher.get('CURRENT_CURR')
        
        if current != None:
            splitted = current.split('_')
        
            measurement_type = splitted[0]
            
            # generate arr only for SPHD (FULL and PREL) normally
            if measurement_type == 'SPHD':
                if a_fetcher.get('SAMPLE_TYPE') == 'SAUNA':
                    self._log.info("Create ARR from SAUNA SAMPML data file for %s" % (a_sid))
               
                    ren = SAUNAXML2HTMLRenderer(self._conf.get('Transformer','templateDir'))
        
                    result = ren.render(a_path)
                    
                    path = "%s/ARR/ARR-%s-%s.html" % (a_dir, a_station_code, a_sid)
                    
                    self._log.info("save file in %s"%(path))
                    
                    ctbto.common.utils.printInFile(result, path)
                    
                elif a_fetcher.get('SAMPLE_TYPE') == 'SPALAX':
                    self._log.info("Create ARR from SPALAX SAMPML data file for %s" % (a_sid))
                   
                    ren = SPALAXXML2HTMLRenderer(self._conf.get('Transformer','templateDir'))
            
                    result = ren.render(a_path)
                    
                    path = "%s/ARR/ARR-%s-%s.html" % (a_dir, a_station_code, a_sid)
                    
                    self._log.info("save file in %s" % (path))
                            
                    ctbto.common.utils.printInFile(result, path)
            else:
                self._log.info("Cannot create a ARR for a sample with a type %s" % (measurement_type))
        else:
            self._log.error("Sample %s hasn't got any CURRENT_CURR in its fetcher"% (a_sid))
        

def run_automatic_tests():
    """ run the automatic test suite """
    
    import ctbto.tests.run_tests as auto_tests
    auto_tests.tests()
    sys.exit(0)

def run_with_args(a_args,exit_on_success=False):
    
    try:
        parsed_args = a_args
        
        Runner.load_configuration(parsed_args)
        
        runner = Runner(parsed_args)
        
        runner.execute(parsed_args) 
    except ParsingError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error()))
        usage() 
        sys.exit(2)
    except ConfAccessError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        if parsed_args.get('verbose',1) == 3:
            print("Traceback: %s."%(get_exception_traceback()))
        usage() 
        sys.exit(2)
    except LoggingSetupError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        sys.exit(2)
    except Exception, e: #IGNORE:W0703,W0702
        try:
            LoggerFactory.get_logger("Runner").error("Error: %s. For more information see the log file %s.\nTry `generate_arr --help (or -h)' for more information."%(e,Conf.get_instance().get('Logging','fileLogging','/tmp/rnpicker.log')))
            if parsed_args.get('verbose',1) == 3:
                a_logger = LoggerFactory.get_logger("Runner").error
            else:
                a_logger = Runner.log_in_file
           
           
            a_logger("Traceback: %s."%(get_exception_traceback()))
        except: 
            print("Fatal error that could not be logged properly. print Traceback in stdout: %s."%(get_exception_traceback())) #IGNORE:W0702
        finally:
            sys.exit(3)
    
    if exit_on_success:
        sys.exit(0)
    else:
        return

def run():
    parsed_args = {}
    
    try:
        parsed_args = parse_arguments(sys.argv[1:])
         
        # very special case: run the automatic case
        # the Runner is bypassed
        if parsed_args['automatic_tests']:
            run_automatic_tests()
            
        Runner.load_configuration(parsed_args)
        
        conf_file = Conf.get_instance().get('log', 'conf_file', '/home/aubert/workspace/RNpicker/etc/conf/logging_rnpicker.config')
         
        runner = Runner(parsed_args)
        runner.execute(parsed_args) 
    except ParsingError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error()))
        usage() 
        sys.exit(2)
    except ConfAccessError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        if parsed_args.get('verbose',1) == 3:
            print("Traceback: %s."%(get_exception_traceback()))
        usage() 
        sys.exit(2)
    except LoggingSetupError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        sys.exit(2)
    except Exception, e: #IGNORE:W0703,W0702
        try:
            LoggerFactory.get_logger("Runner").error("Error: %s. For more information see the log file %s.\nTry `generate_arr --help (or -h)' for more information."%(e,Conf.get_instance().get('Logging','fileLogging','/tmp/rnpicker.log')))
            if parsed_args.get('verbose',1) == 3:
                a_logger = LoggerFactory.get_logger("Runner").error
            else:
                a_logger = Runner.log_in_file
           
            a_logger("Traceback: %s."%(get_exception_traceback()))
        except: 
            print("Fatal error that could not be logged properly. print Traceback in stdout: %s."%(get_exception_traceback())) #IGNORE:W0702
        finally:
            sys.exit(3)
    
    sys.exit(0)
          
if __name__ == "__main__":
    
    run()
    #usage()
