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
import ctbto.common.utils
from org.ctbto.conf    import Conf
from ctbto.db          import DatabaseConnector,DBDataFetcher
from ctbto.renderers   import SaunaRenderer
from ctbto.transformer import XML2HTMLRenderer


VERSION     ="1.0"
DATE_FORMAT = "%Y-%m-%d"

def usage():
    
    print("this is the usage\n")

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

def myBasicLoggingConfig():
    """
    Do basic configuration for the logging system by creating a
    StreamHandler with a default Formatter and adding it to the
    root logger.
    """
    if len(logging.root.handlers) == 0:
        hdlr = logging.handlers.RotatingFileHandler("/tmp/logging.log", "a", 5000000, 4)
        console = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_filter    = logging.Filter('Runner')
        hdlr.setFormatter(fmt)
        
        
        console.setFormatter(console_formatter)
        console.addFilter(console_filter)
        
        logging.root.addHandler(hdlr)
        logging.root.addHandler(console)
        
        #log = logging.getLogger("ROOT")
        #log.setLevel(logging.INFO)

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
    
    try:
        (opts,_) = getopt.getopt(a_args, "hs:f:e:d:c:v", ["help", "s=","from=","end=","dir=","conf_dir=","version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            print("version %s"%(VERSION))
            #sys.exit()
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
                        raise Exception("Error passed sid %s is not a number"%(s)) 
                    
                result['sids'] = sids   
            elif a.isdigit():
                result['sids'] = [a]                
            else:
                raise Exception("Error passed sid %s is not a number"%(a))
        elif o in ("-d", "--dir"):
            # try to make the dir if necessary
            ctbto.common.utils.makedirs(a)
            result['dir'] = a   
        elif o in ("-f", "--from"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a,DATE_FORMAT)
                result['from'] = a
            except:
                raise Exception("Invalid from date %s"%(a))
        elif o in ("-e", "--end"):
            try:
                #check that the passed string a date
                datetime.datetime.strptime(a,DATE_FORMAT)
                result['end'] = a
            except:
                raise Exception("Invalid from date %s"%(a))
        elif o in ("-c", "--conf_dir"):
            try:
                #check that it is a dir
                if not os.path.isdir(a):
                    raise Exception("%s conf_dir is not a directory")
                result['conf_dir'] = a
            except:
                raise Exception("Invalid from date %s"%(a))
        else:
            raise Exception("unknown option %s = %s"%(o,a))
    
    return result

SQL_GETSAUNASAMPLEIDS = "select SAMPLE_ID,STATION_ID,SITE_DET_CODE from GARDS_SAMPLE_DATA where station_id in (522, 684) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s"

class Runner(object):
    """ Class for fetching and producing the ARR """
    
    # Class members
    c_log = logging.getLogger("Runner")
    c_log.setLevel(logging.INFO)


    def __init__(self,a_args):
        
        super(Runner,self).__init__()
          
        # create an empty shell Conf object
        self._conf = self._load_configuration(a_args)
    
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
        
    def _load_configuration(self,a_args):
        """
            try to load the configuration from the config file.
            priority rules: if --conf_dir is set, try to read a dir/rnpicker.config. Otherwise look for SAMPML_CONF_DIR env var
        
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
            dir = os.environ.get('SAMPML_CONF_DIR',None)
        else:
            #always force the ENV Variable
            os.environ['SAMPML_CONF_DIR'] = dir
        
        if dir is None:
            raise Exception('Error. the conf dir needs to be set from the command line or using the env variable SAMPML_CONF_DIR')
        
        if os.path.isdir(dir):
            os.environ[Conf.ENVNAME] = '%s/%s'%(dir,'rnpicker.config')
            
            return Conf.get_instance()
        else:
            raise Exception('Error. The conf dir %s set with the env variable SAMPML_CONF_DIR is not a dir'%(dir))
        
    def _getListOfSaunaSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='1000000'):
        
        result = self._ngMainConn.execute(SQL_GETSAUNASAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        Runner.c_log.info("Found %d sampleIDs: %s\n"%(len(sampleIDs),sampleIDs))
       
        return sampleIDs
    
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
        elif 'from' in a_args or 'end' in a_args:
            begin = a_args.get('from','2009-01-14')
            end   = a_args.get('end','2009-01-14')
            
            sids = self._getListOfSaunaSampleIDs(begin, end)
        else:
            raise Exception('need either a sid or some dates')
    
        dir = a_args['dir']
        
        self._create_directories(dir)
    
        for sid in sids:
    
            Runner.c_log.info("**************************************************")
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
            
            Runner.c_log.info("**************************************************\n")
  
def run():
    #args = '-v -s 211384,211065'.split()
    args = '-v -s 211384 --from 2008-12-02 --end 2008-12-04 --dir /tmp'.split()
    print "args = %s\n"%(args)
    #args = sys.argv[1:]
    
    try:
        parsed_args = parse_arguments(sys.argv[1:])
        
        # setup loggers   
        myBasicLoggingConfig()
    
        #print "result = %s\n"%(parsed_args)
        
        runner = Runner(parsed_args)
        
        runner.execute(parsed_args)
        
    except : #IGNORE:W0703,W0702
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info() #IGNORE:W0702
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback)
        usage()
        sys.exit(3)
          
if __name__ == "__main__":
    print "dir = %s"%(get_tests_dir_path())
    run()
