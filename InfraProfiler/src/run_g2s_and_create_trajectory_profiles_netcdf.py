'''
Created on Sep 1, 2009

@author: guillalume.aubert@ctbto.org
'''
# common packages
import os
import sys
import datetime
import getopt


from org.ctbto.conf import Conf

import utils

import trajectory_const
import error_commons
import g2s_commons
import cli_parsing_commons

NAME        = "run_g2s_and_create_netcdf"
VERSION     = "1.0"
DATE_FORMAT = "%Y-%m-%d"


def usage():
    """ usage function """
    usage_string = """
Usage: run_g2s_and_create_netcdf [options] 

  Mandatory Options:
  --start          (-s)   starting date YYYY-MM-DDTHH
  --end            (-e)   ending date YYYY-MM-DD-HH
  --trajectory     (-t)   trajectory file
  --bin_dir        (-b)   destination dir where the .bin files will be written
  --netcdf_dir     (-n)   destination dir where the netcdf files will be written

  Help Options:
   --help     Show this usage information.

  Examples:
  
  >./run_g2s_and_create_netcdf --from 2009-01-15T00 --end 2009-01-18T00 --bin_dir /tmp/bin_dir --netcdf_dir /tmp/netcdf_dir
  
  Create Infrasound profiles from 2009-01-15 00Hrs until 2009-01-18 00 Hrs (00 hrs is not included).
  Generate .bin results in /tmp/bin_dir and .nc in /tmp/netcdf_dir
 
  """
       
    print(usage_string)
    

def parse_arguments(a_args): #pylint: disable-msg=R0912
    """
            Arguments to parse
            
            Args:
               a_args: list of arguments to parse. 
               
            Returns:
               return a dict containing all the parsed arguments
        
            Raises:
               exception
    """
    
    result = {}
    
    # add defaults
    result['bin_dir']    =  Conf.get_instance().get('G2S', 'gs2_default_bin_dir', '/tmp/bin_dir')
    
    result['netcdf_dir'] = Conf.get_instance().get('G2S', 'gs2_default_necdf_dir', '/tmp/netcdf_dir')
   
    try:
        reassoc_args = cli_parsing_commons.reassociate_arguments(a_args)
        (opts, _) = getopt.gnu_getopt(reassoc_args, "hs:e:b:n:v", ["help", "start=", "end=", "bin_dir=", "netcdf_dir="])
    except Exception, err: #IGNORE:W0703
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            print("%s v %s" % (NAME, VERSION))
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--start"):
            try:
                #check that the passed string a date
                start = get_datetime_from_str(a)
                result['start'] = start
            except:
                raise cli_parsing_commons.ParsingError("Invalid --start or -s date %s"%(a))
        elif o in ("-e", "--end"):
            try:
                #check that the passed string a date
                end = get_datetime_from_str(a)
                result['end'] = end
            except:
                raise cli_parsing_commons.ParsingError("Invalid --end or -e date %s"%(a))
        elif o in ("-b", "--bin_dir"):
            # try to make the dir if necessary
            result['bin_dir'] = a
        elif o in ("-n", "--netcdf_dir"):
            # try to make the dir if necessary
            result['netcdf_dir'] = a    
        elif o in ("-c", "--conf_dir"):
            try:
                #check that it is a dir
                if not os.path.isdir(a):
                    raise cli_parsing_commons.ParsingError("%s --conf_dir or -d is not a directory"%(a))
                result['conf_dir'] = a
            except:
                raise cli_parsing_commons.ParsingError("Invalid --conf_dir or -d %s"%(a))
        else:
            raise cli_parsing_commons.ParsingError("Unknown option %s = %s" % (o , a))
    
    if not result.has_key('start'):
        raise cli_parsing_commons.ParsingError("need a starting date")
        
    if not result.has_key('start'):
        raise cli_parsing_commons.ParsingError("need a end date")
    
    utils.makedirs(result['netcdf_dir'])
    utils.makedirs(result['bin_dir'])
    
    return result

def get_datetime_from_str(a_str_date):
    """
        transform a string into datetime
        
        Args:
           a_str_date: string date
           
        Returns:
           return a datetime
    
        Raises:
           exception
    """
    
    return datetime.datetime.strptime(a_str_date,'%Y-%m-%dT%H')

def load_configuration(a_args):
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
    conf_dir = a_args.get('conf_dir', None)
    
    #try to read from env
    if conf_dir == None:
        conf_dir = os.environ.get('INFRAPROFILER_CONF_DIR', None)
    else: 
        #always force the ENV Variable
        os.environ['INFRAPROFILER_CONF_DIR'] = dir
    
    if conf_dir is None:
        raise error_commons.ConfAccessError('The conf dir needs to be set from the command line or using the env variable RNPICKER_CONF_DIR')
    
    if os.path.isdir(conf_dir):
        os.environ[Conf.ENVNAME] = '%s/%s' % (conf_dir, 'infra_profiler.config')
        
        return Conf.get_instance()
    else:
        raise error_commons.ConfAccessError('The conf dir %s set with the env variable INFRAPROFILER_CONF_DIR is not a dir' % (dir))



def _get_station_info():
    """ get station coordinates """


    names  = []
    lats   = []
    lons   = []
    
    for station in trajectory_const.REB_TRAJECTORY:
        (lat, lon) = trajectory_const.REB_TRAJECTORY[station]
        
        lats.append(lat)
        lons.append(lon)
        names.append(station)
    
    return (names, lats, lons)


def do_run(path, args, lats, lons, sta_names):
    """ do run """
    print("===================================================================\n")
           
    print("Generation for %s \n" %(path) )
        
    (f107, f107a, ap) = g2s_commons.get_noaa_indices(path)
    
    bin_file_path = g2s_commons.run_g2s(args['bin_dir'], path, f107, f107a, ap)
    
    print("bin_file_path %s\n" %(bin_file_path))
    
    g2s_commons.call_g2s_client(args['netcdf_dir'],bin_file_path, path, lats, lons, sta_names)
            
    print("===================================================================\n")
      
if __name__ == "__main__":
    
    
    try:
        args = {}
        
        load_configuration(args)
        
        args = parse_arguments(sys.argv[1:])
        
        ecmwf_data_paths = g2s_commons.get_ecmwf_data(args['start'], args['end'])
        
        print("BIN files written in %s\n" % (args['bin_dir']) )
        print("netcdf files written in %s\n" %(args['netcdf_dir']) )                                
        
        print("Ecmwf data paths %s\n" %(ecmwf_data_paths))
        
        (sta_names, lats, lons) = _get_station_info()
    
        for path in ecmwf_data_paths:
            time_spent = utils.ftimer(do_run, [path, args, lats, lons, sta_names], {})
            
            print("Generation for %s done in %.2f seconds \n" %(path, time_spent) )
        
    except cli_parsing_commons.ParsingError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error()))
        usage() 
        sys.exit(2)
    except error_commons.ConfAccessError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        if args.get('verbose', 1) == 3:
            print("Traceback: %s."%(error_commons.get_exception_traceback()))
        usage() 
        sys.exit(2)
        
        
        

        
        
    
    