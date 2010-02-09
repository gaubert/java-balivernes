""" 
    Copyright 2008 CTBTO Organisation
    
    module: generate_noble_gaz_arr
"""

import getopt, sys
import os
import tarfile
import zipfile
import pickle
import datetime
import logging.handlers
import StringIO
import traceback
import shutil


import ctbto.common.time_utils
from ctbto.common.logging_utils import LoggerFactory
import ctbto.common.utils
from org.ctbto.conf    import Conf
from ctbto.db          import DatabaseConnector
import ctbto.run.generate_arr as arr_generator
from ctbto.email import DataEmailer

NAME        = "generate_and_email"
VERSION     = "0.6"
DATE_FORMAT = "%Y-%m-%d"

def usage():
    
    usage_string = """
Usage: generate_and_email [options] 

  Mandatory Options:
  --group          (-g)   The email group (or alias) as defined in the configuration group
                          [AutomaticEmailingGroups]. This group defines a set of emails
                          to whom send the data once generated         
  Extra Options:
  --dir             (-d)  Destination directory where the data will be written.                     (default="/tmp/generate_and_email_data")
                          The SAMPML files will be added under DIR/samples and the ARR
                          under DIR/ARR. 
                          The directories will be created if not present.
                          
  --conf_dir        (-c)  Directory containing a configuration file rnpicker.config.                (default=$RNPICKER_CONF_DIR)  
  
  --vvv             (-3)  Increase verbosity to level 3 in order to have all the errors
                          in the stdout.  
  
  Advanced Options:
  --from            (-f)  Retrieve and send all samples from this date.
                          In that case the oldest date in the group db is ignored.
                          The date is in the YYYY-MM-DD form (ex: 2008-08-22).
  
  --force           (-r)  All the samples for all the dates are resent
  
  --clean_group_db  (-o)  Delete the group database file that keeps track of what has been sent the
                          group defined by --group or -g option.


  Help Options:
   --help     Show this usage information.

  Examples:
  >./generate_and_email --group test --dir ./test-data 
  
  Get all SAUNA and SPALAX data and send them to the users in the group test starting from today (by default)
  
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

def reassociate_arguments(a_args):
    """
        reassociate arguments passed in the program arguments when they are spearated by a space.
        a, b , c will become 'a, b ,c'
    """
    l = len(a_args)
    
    if l <= 1:
        return a_args
    else:
        res = []
        _reassoc_arguments(a_args[0],a_args[1:],res)
        return res

def _reassoc_arguments(head,tail,res,memo=''): 
    """
            private function used to recurse in reassociate_arguments
    """
    # stop condition, no more fuel
    if len(tail) == 0:
        # if command separate
        if head.startswith('-'):
            res.extend([memo,head])
            return
        else:
            res.append(memo + head)
            return
    
    if head.endswith(',') or head.startswith(','):
        _reassoc_arguments(tail[0],tail[1:] if len(tail) > 1 else [],res,memo+head)
    elif head.startswith('-'):
        # we do have a command so separate it from the rest
        if len(memo) > 0:
            res.append(memo)
            
        res.append(head)
        
        _reassoc_arguments(tail[0],tail[1:] if len(tail) > 1 else [],res,'')
    else:  
        # it is not a command 
        _reassoc_arguments(tail[0],tail[1:] if len(tail) > 1 else [],res,memo+head) 
            
    

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
    
    # --id 
    # look for list for the current day and compute it
    
    result = {}
    
    # add defaults
    result['dir']                 = "/tmp/generate_and_email_data"
    result['verbose']             = 1
    result['automatic_tests']     = False
    result['station_types']       = ['SAUNA','SPALAX']
    result['force_send']          = False
    result['clean_group_db']      = False
    result['from']                = None
    
    try:
        reassoc_args = reassociate_arguments(a_args)
        (opts,_) = getopt.gnu_getopt(reassoc_args, "horg:d:c:f:v3", ["help","from=","force","clean_group_db","group=","dir=","conf_dir=","version","vvv"])
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
        elif o in ("-g", "--group"):
            result['id'] =  a     
        elif o in ("-d", "--dir"):
            # try to make the dir if necessary
            ctbto.common.utils.makedirs(a)
            result['dir'] = a   
        elif o in ("-f", "--from"):
            try:
                #check that the passed string a date
                d = datetime.datetime.strptime(a,DATE_FORMAT)
                
                result['from'] = ctbto.common.time_utils.getISO8601fromDateTime(d)
                
            except:
                raise ParsingError("Invalid --from or -f date %s"%(a))
        elif o in ("-3","--vvv"):
            result['verbose'] = 3
        elif o in ("-r","--force"):
            result['force_send'] = True
        elif o in ("-o","--clean_group_db"):
            result['clean_group_db'] = True  
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
        else:
            raise ParsingError("Unknown option %s = %s"%(o,a))
    
    return result

# Using collection_stop as time reference but it is an issue because some times the samples are received several days after
#SQL_GETSAMPLEIDS                   = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (%s) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"
#transmit DTG should be the time reference we can only send in realtime what we receive
# also select only SPHDF 
SQL_GETSAMPLEIDS                   = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (%s) and (TRANSMIT_DTG between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and data_type not in ('Q','D','G','C') and ROWNUM <= %s order by SAMPLE_ID"

# original
#SQL_GETALLSAUNASTATIONCODES        = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where type='SAUNA' or type='ARIX-4'"
# remove EU stations
SQL_GETALLSAUNASTATIONCODES        = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where (type='SAUNA' or type='ARIX-4') and station_code not like '%EU%'"

SQL_GETALLSPALAXSTATIONCODES       = "select STATION_CODE,STATION_ID from RMSMAN.GARDS_STATIONS where type='SPALAX'"

SQL_GETALLSTATIONIDSFROMCODES      = "select STATION_ID from RMSMAN.GARDS_STATIONS where station_code in (%s)"

SAMPLES_KEY    = "sent_samples"
HISTORY_KEY    = "history"
LAST_TIME_SENT = "last_time"

class CLIError(Exception):
    """ Base class exception """
    pass

class ParsingError(CLIError):
    """Error when the command line is parsed"""

    def __init__(self,a_error_msg):
        super(ParsingError,self).__init__()
        self._error_message = a_error_msg
        
    def get_message_error(self):
        return self._error_message
        
class ConfAccessError(CLIError):
    """The only exception where a logger as not yet been set as it depends on the conf"""

    def __init__(self,a_error_msg):
        super(ConfAccessError,self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        return self._error_message

class LoggingSetupError(CLIError):
    """Error when the logger cannot be setuped"""

    def __init__(self,a_error_msg):
        super(LoggingSetupError,self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        return self._error_message

class Runner(object):
    """ Class for fetching and producing the ARR """
    
    def __init__(self,a_args):
        
        super(Runner,self).__init__()
          
        # create an empty shell Conf object
        self._conf     = self._load_configuration(a_args)
        
        self._log = LoggerFactory.get_logger("Runner")
    
        # setup the prod database and connect to it
        self._ngDatabase        = self._conf.get("NobleGazDatabaseAccess","hostname")
        self._ngUser            = self._conf.get("NobleGazDatabaseAccess","user")
        self._ngPassword        = self._conf.get("NobleGazDatabaseAccess","password")
        self._ngActivateTimer   = self._conf.getboolean("NobleGazDatabaseAccess","activateTimer",True)
   
        # create DB connector
        self._ngMainConn = DatabaseConnector(self._ngDatabase,self._ngUser,self._ngPassword,self._ngActivateTimer)

        # setup the archive database and connect to it
        self._ParticulateArchiveDatabaseAccess       = self._conf.get("ParticulateArchiveDatabaseAccess","hostname")
        self._archiveUser           = self._conf.get("ParticulateArchiveDatabaseAccess","user")
        self._archivePassword       = self._conf.get("ParticulateArchiveDatabaseAccess","password")
        self._archiveActivateTimer  = self._conf.getboolean("ParticulateArchiveDatabaseAccess","activateTimer",True)
        
        # create DB connector
        self._ngArchConn = DatabaseConnector(self._ParticulateArchiveDatabaseAccess,self._archiveUser,self._archivePassword,self._archiveActivateTimer)
        
        #connect to the DBs
        self._ngMainConn.connect()
        self._ngArchConn.connect()
    
    @classmethod
    def log_in_file(self,aMessage):
        """ to log in the file as the ROOT logger """
        
        log = LoggerFactory.get_logger("ROOT")
        log.info(aMessage)
        
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
    
    def _create_temp_directories(self,dir):
        
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s/data'%(dir))
        
    def _create_db_directories(self,dir):
        
        # try to make the dir if necessary
        ctbto.common.utils.makedirs('%s'%(dir))   
    
    def _get_list_of_sampleIDs(self,stations='',beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='10000000'):
        
        l = ','.join(map(str,stations)) #IGNORE:W0141
        
        result = self._ngMainConn.execute(SQL_GETSAMPLEIDS%(l,beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        self._log.info("There are %d products (samples) for the %s."%(len(sampleIDs),beginDate.split(' ')[0]))
        self.log_in_file("List of sampleIDs to fetch: %s"%(sampleIDs))
        
        sampleIDs.sort()
        
        return  sampleIDs

    def _get_all_stations(self,a_stations_types):
        
        sta_ids    = []
        
        for type in a_stations_types:
        
            if   type == 'SAUNA':
                result = self._ngMainConn.execute(self._conf.get("Products","Sauna_Stations_SQL",SQL_GETALLSAUNASTATIONCODES))
            elif type == 'SPALAX':
                result = self._ngMainConn.execute(self._conf.get("Products","Spalax_Stations_SQL",SQL_GETALLSPALAXSTATIONCODES))
        
            sta_codes  = []
           
            rows   = result.fetchall()
        
            for row in rows:
                sta_codes.append(row[0])
                sta_ids.append(row[1])
            
            self._log.info("Found %d %s stations."%(len(sta_codes),type))
            self.log_in_file("Found the following %s stations: %s."%(type,sta_codes))
        
        return sta_ids
    
    def _get_list_of_days_to_search(self,a_db_dict,a_from):
        """ 
           return list of days to search using the db_dict content.
           If a_from is passed and valid use as the from_date.
           If there are some days in db_dict set the from_date from this point.
           If not use today.
        
           Args:
               a_db_dict       : Persistent dictionary containing what has already been sent
               
            Returns:
               
        
            Raises:
               exception
        """
        list_of_days = []
        iso_from_day = None
        
        # no from date so look in the group_db to find the oldest date
        # if no date has been found use the first date as today
        if a_from == None:
            l_keys = a_db_dict.keys()
            if len(l_keys) > 0:
                iso_from_day = min(l_keys)
            else:
                iso_from_day = ctbto.common.time_utils.getToday() 
        else:
            iso_from_day = a_from
        
        from_datetime = ctbto.common.time_utils.getDateTimeFromISO8601(iso_from_day)
        
        now_datetime  = datetime.datetime.today()
        
        nb_days = (now_datetime - from_datetime).days
        
        # normal case nb_days is >= 0
        if nb_days >= 0:
            # iterate over the date days
            cpt = 0
            temp_datetime = from_datetime
            while cpt <= nb_days:
                list_of_days.append(ctbto.common.time_utils.getISO8601fromDateTime(temp_datetime))
                temp_datetime = temp_datetime + datetime.timedelta(days=1)
                cpt += 1
        else:
            self._log.info("Error nb_days should >=0")
            
        return list_of_days
    
    def _get_list_of_new_samples_to_email(self, a_db_dict, a_list_of_days, a_station_types,force_resend=False):
        """
            Method returning what samples needs to be sent an fetched for a particular day.
            The day is designated by searched_day.
        
            Args:
               a_db_dict       : Persistent dictionary containing what has already been sent
               a_searched_day  : Searched day (usually dd:mm:yyT00:00:00). It is a datetime object
               
            Returns:
              
        
            Raises:
               exception
        """
        
        # get all related stations
        stations      = self._get_all_stations(a_station_types)
        
        result = {}
        
        # for each day check if there is more samples to retrieve that what is in the db
        # if yes add the new samples to the list of samples to fetch
        for day in a_list_of_days:
            
            begin_date = ctbto.common.time_utils.getDateTimeFromISO8601(day)
            end_date   = begin_date + datetime.timedelta(days=1)
            
            # get them in Oracle format
            d1 = ctbto.common.time_utils.getOracleDateFromDateTime(begin_date)
            d2 = ctbto.common.time_utils.getOracleDateFromDateTime(end_date)
            
            # get list of samples for the chosen day
            l        = self._get_list_of_sampleIDs(stations,d1,d2)
            
            if not force_resend:
                l_set    = set(l)
            
                # get previous list
                if day in a_db_dict:
                    l_prev_set = set(a_db_dict[day][SAMPLES_KEY])
                    new_samples_set = l_set.difference(l_prev_set)
                else:
                    new_samples_set = l_set
            
                if len(new_samples_set) > 0:
                    l = list(new_samples_set)
                    l.sort()   
                    self._log.info("%d new products to be retrieved for %s."%(len(l),day))
                    result[day] = l
            else:
                l.sort()
                if len(l) > 0:
                    self._log.info("Will fetch the %d new products for %s."%(len(l),day))
                result[day] = l
                
        # print all values
        full_list = []
        for value in result.itervalues():
            full_list.extend(value)
        
        if len(full_list) > 0:
            full_list.sort()
            Runner.log_in_file("Will fetch the following sampleIDs"%(full_list))
        
        return result
               
    def _save_in_id_database(self,a_id,a_dir,a_db_dict,a_emailed_list,a_searched_day,a_sending_time_stamp):
        """
            Save the information related to the current batch in the db_dict.
            
            Args:
               a_id                 : email group name,
               a_dir                : directory where the db_dict is going to be stored,
               a_db_dict            : Persistent dictionary containing what has already been sent,
               a_emailed_list       : Searched day (usually dd:mm:yyT00:00:00). It is a datetime object,
               a_searched_day       : the day for which the samples are retrieved (key in db_dict)
               a_sending_time_stamp : timestamp when the data was sent (key for the history) 
               
            Returns:
               None
        
            Raises:
               exception
        """
        key = a_searched_day
        
        # if it doesn't exist, initialize the structure
        if key not in a_db_dict:
            a_db_dict[key] = {}
            a_db_dict[key][SAMPLES_KEY]    = []
            a_db_dict[key][HISTORY_KEY]    = {}
            a_db_dict[key][LAST_TIME_SENT] = None
            
            
        info_dict = a_db_dict.get(key,{})
        
        l = info_dict.get(SAMPLES_KEY,[])
        
        l.extend(a_emailed_list) 
        
        a_db_dict[key][SAMPLES_KEY] = l
        
        # Add history info
        hist_d = info_dict[HISTORY_KEY]
        
        hist_d[a_sending_time_stamp] = a_emailed_list
        
        a_db_dict[key][LAST_TIME_SENT] = a_sending_time_stamp
        
        filename = "%s/%s.emaildb"%(a_dir,a_id)
        
        f = open(filename,'w')
        
        pickle.dump(a_db_dict,f) 
        
        f.close()
        
    def _remove_expired_days_from_db_dict(self,a_db_dict,a_dir,a_id):
        """ 
            remove all samples that are older than the limit given in the config file 
        """
        self._log.info("Remove information from the group database %s/%s.emaildb if expired"%(a_dir,a_id))
        
        limit = self._conf.getint('AutomaticEmailingInformation','expirationDate',20)
            
        keys = a_db_dict.keys()
        
        keys.sort()
        
        now_datetime  = datetime.datetime.today()
        
        '''
        for key in keys:
            a_db_dict[key][LAST_TIME_SENT] = '2009-03-25T173546'
            
            filename = "%s/%s.emaildb"%(a_dir,a_id)
        
            f = open(filename,'w')
        
            pickle.dump(a_db_dict,f) 
            
            f.close()
        '''
            
        
        for key in keys:
            # get a datetime so nothing to do
            timestamp = a_db_dict[key].get(LAST_TIME_SENT,None)
            
            # to be compatible with the previous version
            # if no LAST_TIME_SENT get now time
            if timestamp == None:
                timestamp = self._get_now_timestamp()
                a_db_dict[key][LAST_TIME_SENT] = timestamp
        
            d = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H%M%S')
        
            diff = now_datetime - d
            if diff.days >= limit:
                self._log.info("Remove %s day information from the group database as now sending have been done for the last %s days."%(key,limit))
                del a_db_dict[key]
            
    def _get_id_database(self,a_dir,a_id):
        """
            return a persistent list if it was stored previously in the db dir. This file should contain a dict of the last five email shots
        
            Args:
               None 
               
            Returns:
               return list object
        
            Raises:
               exception
        """
        filename = "%s/%s.emaildb"%(a_dir,a_id)
        
        data = {}
        
        if os.path.exists(filename):
            f = open(filename)
            data = pickle.load(f)
            f.close()
            
        return data
    
    def _move_sent_files_to_files_db(self,a_origin_dir,a_destination_dir):
        """
           move all files from a_origin_dir in a_destination_dir and delete the a_origin_dir
        """
        try:
            for root,dirs,_ in os.walk(a_origin_dir):
                for dir in dirs:
                    if dir in ['ARR','samples']:
                        dest = '%s/%s'%(a_destination_dir,dir)
                        for i_r,_,i_files in os.walk('%s/%s'%(root,dir)):
                            # only consider files in ARR and in samples
                            for filename in i_files:
                                shutil.move('%s/%s'%(i_r,filename),dest)
             
        except Exception, e: #IGNORE:W0703,W0702
            # hide error in logs because it is a minor error
            self._log.debug("Error when trying to move retrieved files from %s into %s.Raised Exception %s"%(a_origin_dir,e))
        finally:
            try:
                # try to delete a_origin_dir even if there was an error
                ctbto.common.utils.delete_all_under(a_origin_dir)
            except Exception, e: #IGNORE:W0703,W0702
                # hide error in logs because it is a minor error
                self._log.debug("Error when trying to delete the directory %s.Raised Exception %s"%(a_origin_dir,e))
           
    def _move_sent_tarfile_to_files_db(self,a_tarfile,a_destination_dir,dir_to_delete):
        """
           move the a_origin_dir in a_destination_dir and delete the a_origin_dir
        """
        try:
            if os.path.exists(a_tarfile):
                shutil.move(a_tarfile,a_destination_dir)
        except Exception, e: #IGNORE:W0703,W0702
            # hide error in logs because it is a minor error
            self._log.debug("Error when trying to move retrieved files from %s into %s.Raised Exception %s"%(dir_to_delete,a_destination_dir,e))
        finally:
            # clean the dirs
            try:
                # try to delete a_origin_dir even if there was an error
                ctbto.common.utils.delete_all_under(dir_to_delete,delete_top_dir=True)
            except Exception, e: #IGNORE:W0703,W0702
                # hide error in logs because it is a minor error
                self._log.debug("Error when trying to delete the directory %s.Raised Exception %s"%(dir_to_delete,e))
            

    def _clean_group_db(self,a_dir,a_id):
        """ clean group db """
        
        self._log.info("Clean file %s"%("%s/%s.emaildb"%(a_dir,a_id)))
        
        path = "%s/%s.emaildb"%(a_dir,a_id)
        
        if os.path.exists(path):
            os.remove(path)
            
    def _create_archive(self,a_archive_filename,a_dir_data):
        """ create the archive that will be sent to the users """
        
        arch_type = self._conf.get('AutomaticEmailingInformation','archiveType','tar')
        
        arch_name = None
        
        self._log.info("*************************************************************")
        
        if arch_type == 'zip':
            self._log.info("Create a zip archive file")       
            arch_name = "%s.zip"%(a_archive_filename)
            z = zipfile.ZipFile(arch_name,"w",zipfile.ZIP_DEFLATED)
            for f_name in ctbto.common.utils.dirwalk(a_dir_data):
                z.write(f_name, arcname=os.path.basename(f_name))
            z.close()
        elif arch_type == 'tar' or arch_type == 'tar.gz':
            self._log.info("Create a tar.gz archive file")
            arch_name = "%s.tar.gz"%(a_archive_filename)
            t = tarfile.open(name = arch_name, mode = 'w:gz')
            t.add(a_dir_data,arcname=os.path.basename(a_dir_data))
            t.close()
        else:
            self._log.info("Unknown archive type %s. Create a tar.gz archive file."%(arch_type))
            arch_name = "%s.tar.gz"%(a_archive_filename)
            t = tarfile.open(name = arch_name, mode = 'w:gz')
            t.add(a_dir_data,arcname=os.path.basename(a_dir_data))
            t.close()
            
        self._log.info("*************************************************************\n")
            
        return arch_name
        
    
    def _send_products_for_each_day(self,day,list_to_fetch,tarfile_name_prefix,dir_to_send,id,dir_files_db,timestamp_id):
        """ send the created products to the users """
        
        # keep only the date part
        printable_day = day.split('T')[0]
        
        self._log.info("*************************************************************\n")
        
        self._log.info("[%s] Get following new samples: %s."%(printable_day,list_to_fetch))
        
        # Call the data fetcher with the right arguments
        args = {}                      
        
        args['dir']                     = dir_to_send
        args['verbose']                 = 1
        args['always_recreate_files']   = False
        args['clean_cache']             = False
        args['automatic_tests']         = False
        args['clean_local_spectra']     = False
        args['sids']                    = list_to_fetch
            
        self._log.info("*************************************************************")
        self._log.info("Call product generator")
        self._log.info("*************************************************************")
        
        arr_generator.run_with_args(args)
        
        # directory containing the data
        # restrict to samples
        if self._conf.getboolean('Products','withARR',False):
            dir_data = "%s" % (dir_to_send)
        else:
            dir_data = "%s/samples"%(dir_to_send)
        
        #create archive and return complete filename (full path and extension: .zip or .tar.gz)
        archfile_name = self._create_archive("%s-%s"%(tarfile_name_prefix,printable_day), dir_data)
            
        groups = [id]
        
        # send email
        emailer = DataEmailer(self._conf.get('AutomaticEmailingInformation','host'),self._conf.get('AutomaticEmailingInformation','port'))
        
        if self._conf.get('AutomaticEmailingInformation','obfuscatePassword', True):
            password = ctbto.common.utils.deobfuscate_string(self._conf.get('AutomaticEmailingInformation','password'))
        else:
            password = self._conf.get('AutomaticEmailingInformation','password')
            
        emailer.connect(self._conf.get('AutomaticEmailingInformation','user'),password)
            
        sender  = self._conf.get('AutomaticEmailingInformation','sender',None)
            
        # the text message that will apear in the email
        text_message = 'The following %d samples from day %s are in the attached tar file %s\nList of samples : %s'%(len(list_to_fetch),printable_day,archfile_name,list_to_fetch)
        
        for group in groups:
            
            emails = self._conf.get('AutomaticEmailingGroups',group,None)
            if emails is None:
                raise Exception('group %s is None in [AutomaticEmailingGroups]'%(group))
                
            self._log.info("*************************************************************")
            self._log.info("Send Email to users %s in group %s"%(emails,group))
            self._log.info("*************************************************************")
                
            emailer.send_email_attached_files(sender,emails,[archfile_name], '[%s:%s]. %d samples retrieved for %s'%(group,timestamp_id,len(list_to_fetch),printable_day),text_message)
        
        # cleaning the file business
        self._move_sent_tarfile_to_files_db(archfile_name,'%s'%(dir_files_db),dir_to_send)
               
    
    def _get_now_timestamp(self):
        """ utility method to return a now timestamp stringified """
        
        # timestamps for create the batch name
        # create sending timestamp (used in the tar.gz file name)
        sending_timestamp = '%s'%(datetime.datetime.now())
        # replace spaces with T and : with nothing
        sending_timestamp = sending_timestamp.replace(' ','T')
        sending_timestamp = sending_timestamp.replace(':','')
        # remove milliseconds
        sending_timestamp = sending_timestamp.split('.')[0]
        
        return sending_timestamp
    
    def execute(self,a_args):
        if a_args == None or a_args == {}:
            raise Exception('No commands passed. See usage message.')
        
        self._log.info("*************************************************************")
        self._log.info("Configuration infos read from %s"%(self._conf.get_conf_file_path()))
        
        self._log.info("*************************************************************\n")
        
        # check if we have some sids or we get it from some dates
        self._log.info("*************************************************************")
        
        if not 'id' in a_args:
            # no actions performed error
            raise Exception('No groups given. Need a group name') 
        else:  
            
            # check that the group id is correct
            id = a_args['id']
            
            if not self._conf.has_option('AutomaticEmailingGroups',id):
                raise Exception('There is no email groups in the configuration ([AutomaticEmailingGroups]) with value %s.'%(id))
        
            # check if we can write in case the dir already exists    
            dir           = a_args['dir']
            # kind of historic of what has been sent
            dir_files_db  = "%s/data" % (dir)
        
            # the dir for the group db. If there is no dir defined in config then take dir as the root dir
            dir_group_db  = "%s/db"%(self._conf.get("AutomaticEmailingInformation","groupDBPath",dir))
        
            sending_timestamp = self._get_now_timestamp()
            
            dir_to_send   = "%s/%s"%(dir,sending_timestamp)
        
            tarfile_name_prefix = "%s/samples_%s"%(dir,sending_timestamp)
  
            # create the necessary directories
            self._create_db_directories(dir)
            self._create_temp_directories(dir_group_db)
            
            if a_args['clean_group_db']:
                self._clean_group_db(dir_group_db,id) 
            
            db_dict = self._get_id_database(dir_group_db,id)
            
            # remove expired days 
            self._remove_expired_days_from_db_dict(db_dict,dir_group_db,id)
            
            list_of_searched_days = self._get_list_of_days_to_search(db_dict,a_args['from'])
            
            #types of stations
            station_types = self._conf.getlist("Products","stations_types","SAUNA,SPALAX")
             
            list_to_fetch = self._get_list_of_new_samples_to_email(db_dict,list_of_searched_days,station_types,a_args['force_send']) 
        
        if len(list_to_fetch) > 0:    
            
            # send a separate email for each day 
            keys = list_to_fetch.keys()
            keys.sort()
            for key in keys:
                self._send_products_for_each_day(key,list_to_fetch[key],tarfile_name_prefix,dir_to_send,id,dir_files_db,sending_timestamp)
                
                self._save_in_id_database(id,dir_group_db,db_dict,list_to_fetch[key],key,sending_timestamp)
                     
        else:
            self._log.info("No new products to send for group %s"%(id))

def run():
    parsed_args = {}
    
    try:
        parsed_args = parse_arguments(sys.argv[1:])
         
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
                a_logger = LoggerFactory.get_logger("Runner")
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
