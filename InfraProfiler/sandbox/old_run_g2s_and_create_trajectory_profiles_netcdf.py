'''
Created on Sep 1, 2009

@author: guillalume.aubert@ctbto.org
'''
# common packages
import os
import sys
import datetime
import getopt
import traceback

import re
import cStringIO
import StringIO
from   subprocess import Popen, PIPE, call

from   ctypes import *

from   netCDF4 import Dataset, date2num, stringtoarr
import time
import string #pylint: disable-msg=W0402
import numpy

from org.ctbto.conf import Conf

from utils import CLIError, ConfAccessError, ffind, makedirs, ftimer
import trajectory_const

NAME        = "run_g2s_and_create_netcdf"
VERSION     = "1.0"
DATE_FORMAT = "%Y-%m-%d"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=====
# To manage arguments

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

class ParsingError(CLIError):
    """Error when the command line is parsed"""

    def __init__(self, a_error_msg):
        super(ParsingError, self).__init__()
        self._error_message = a_error_msg
        
    def get_message_error(self):
        """ return error message """
        return self._error_message

def usage():
    """ usage function """
    usage_string = """
Usage: run_g2s_and_create_netcdf [options] 

  Mandatory Options:
  --start          (-s)   starting date YYYY-MM-DDTHH
  --end            (-e)   ending date YYYY-MM-DD-HH
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
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo + head)
    elif head.startswith('-'):
        # we do have a command so separate it from the rest
        if len(memo) > 0:
            res.append(memo)
            
        res.append(head)
        
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, '')
    else:  
        # it is not a command 
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo + head) 
            
    

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
        reassoc_args = reassociate_arguments(a_args)
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
                raise ParsingError("Invalid --start or -s date %s"%(a))
        elif o in ("-e", "--end"):
            try:
                #check that the passed string a date
                end = get_datetime_from_str(a)
                result['end'] = end
            except:
                raise ParsingError("Invalid --end or -e date %s"%(a))
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
                    raise ParsingError("%s --conf_dir or -d is not a directory"%(a))
                result['conf_dir'] = a
            except:
                raise ParsingError("Invalid --conf_dir or -d %s"%(a))
        else:
            raise ParsingError("Unknown option %s = %s" % (o , a))
    
    if not result.has_key('start'):
        raise ParsingError("need a starting date")
        
    if not result.has_key('start'):
        raise ParsingError("need a end date")
    
    makedirs(result['netcdf_dir'])
    makedirs(result['bin_dir'])
    
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
        raise ConfAccessError('The conf dir needs to be set from the command line or using the env variable RNPICKER_CONF_DIR')
    
    if os.path.isdir(conf_dir):
        os.environ[Conf.ENVNAME] = '%s/%s' % (conf_dir, 'infra_profiler.config')
        
        return Conf.get_instance()
    else:
        raise ConfAccessError('The conf dir %s set with the env variable INFRAPROFILER_CONF_DIR is not a dir' % (dir))


def get_files_from(a_dir, a_file_list):
    """
        Return a list of files from the location with the full location path.
     
        Args:
          a_dir: starting dir where to look for
          a_file_list: list of files to look for
          
        Returns:
           list of file from production location
    
        Raises:
           exception
    """
    print("get list of files from location %s\n" %( a_dir ))
    
    result = ffind(a_dir, shellglobs = a_file_list )
    
    return result

def build_list_of_filenames(a_start_date, a_end_date):
    """
     Get list of files
     
     Args:
          a_start: starting date (included)
          a_end  : end date (included)
           
        Returns:
           return list of file names
    
        Raises:
           exception
    """
    result = []
    
    current_date = a_start_date
    
    # get step from conf
    step = datetime.timedelta(hours=Conf.get_instance().getint('ECMWFDATA', 'time_step', 3))

    while current_date < a_end_date:
        result.append('EN%s' % (current_date.strftime('%y%m%d%H') ) )
        # add step
        current_date += step
    
    return result
        

def get_ecmwf_data(a_start, a_end):
    """
     Find all ECMWF data within a given period.
     Look first in prod then in archive
     
     Args:
          a_start: starting date (included)
          a_end  : end date (included)
           
        Returns:
           return 
    
        Raises:
           exception
    """
    result = []
    
    filenames = build_list_of_filenames(a_start, a_end)
    
    print('filenames = %s\n' % (filenames) )
    
    conf = Conf.get_instance()
    
    prod_dir = conf.get('ECMWFDATA', 'production_loc')
    arch_dir = conf.get('ECMWFDATA', 'archive_loc')
    
    prod_list = []
    arch_list = []
    
    # best effort policy try to get all possible files
    try:
        prod_list = get_files_from(prod_dir, filenames)
    except Exception, exc: #pylint: disable-msg=W0703
        print("Warning. Error: %s\n" %(exc) )
     
    if conf.get('ECMWFDATA','check_in_archive', False): 
        try:
            arch_list = get_files_from(arch_dir, filenames)
        except Exception, exc: #pylint: disable-msg=W0703
            print("Warning. Error: %s\n" %(exc) )
    
    
    print('files found in prod %s\n' %(prod_list) )
    print('files found in arch %s\n' %(arch_list) )

    result.extend(prod_list)
    result.extend(arch_list)
    
    return result

def get_datetime_from_ecmwf_file_name(a_ecmwf_file_name):
    """
    
    """
    str_date = os.path.basename(a_ecmwf_file_name)
    str_date = str_date[2:]
    
    the_date = datetime.datetime.strptime(str_date, '%y%m%d%H')
    
    return the_date

def get_noaa_indices(a_ecmwf_file_name):
    """
       get noaa indices for a particular date.
       This calls a scripts that gets the data from NOAA web site
       
       Args:
          a_ecmwf_file_name : ecmwf file name starting with EN
    """
    
    # create a datetime from the ECMWF filename and convert it in NOAA form '%Y%m%d'
    noaa_date = get_datetime_from_ecmwf_file_name(a_ecmwf_file_name).strftime('%Y%m%d')
    
    conf = Conf.get_instance()
    
    the_dir = conf.get('NOAADATA', 'dir')
    exe     = conf.get('NOAADATA', 'exe')
    
    exe = re.sub(r'\${date}', noaa_date , exe)
    exe = re.sub(r'\${dir}', the_dir , exe)
    
    command = '%s/%s' % (the_dir, exe)
    
    print('will run [%s]\n' % (command) )
    
    # call the command
    pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    
    # call and wait for it to stop
    stdout, stderr = pipe.communicate()
    
    if pipe.returncode != 0:
        #error for this file
        print("Cannot get NOAA data for %s.\nError = \n[%s]\n"%(a_ecmwf_file_name, stderr))
        
        raise Exception("Cannot get NOAA data for %s.\nError = \n[%s]\n"%(a_ecmwf_file_name, stderr))
    else:
        the_fh = cStringIO.StringIO(stdout)
        
        f107  = ""
        f107a = ""
        ap    = ""
        
        cpt = 0
        for line in the_fh:
            if cpt == 0:
                f107 = line.strip()
            elif cpt == 1:
                f107a = line.strip()
            elif cpt == 2:
                ap = line.strip()
            cpt += 1
        
        print("noaa indices = %s,%s,%s\n" %(f107, f107a, ap))
        return (f107, f107a, ap)

def run_g2s(a_output_dir, a_filename, a_f107, a_f107a, a_ap):
    """
    $g2smodel_dir/$g2smodel -v -d $output_dir -i $F107 $F107a $Ap $ECMWF_ops/$ENfilename >& $logdir/$g2s_logfile
    """
    conf = Conf.get_instance()
    
    #get info from conf          
    log_dir    = conf.get('G2S','g2s_log_dir')
    #the_dir    = conf.get('G2S', 'dir')
    exe        = conf.get('G2S', 'exe')
    
    log_file = '%s/g2s_%s.log' % (log_dir, os.path.basename(a_filename))
    
    print("log_dir = %s\n" % (log_dir))
    print("output_dir = %s\n" % (a_output_dir) )
    
    # makedirs
    makedirs(a_output_dir)
    makedirs(log_dir)
    
    #check if the bin file already exists. If yes don't do anything
    the_date = get_datetime_from_ecmwf_file_name(a_filename)
    bin_file = 'G2SGCSx%s_HWM07.bin' % (the_date.strftime('%Y%m%d%H'))
    
    # look for bin_file    
    if not os.path.exists('%s/%s' % (a_output_dir, bin_file)) :
 
        # substitute command line
        exe = re.sub(r'\${log_file}', log_file, exe)
        exe = re.sub(r'\${output_dir}', a_output_dir, exe)
        
        # substitue params
        exe = re.sub(r'\${f107}', a_f107, exe)
        exe = re.sub(r'\${f107a}', a_f107a , exe)
        exe = re.sub(r'\${ap}', a_ap, exe)
        # substitute ecmwf file
        exe = re.sub(r'\${ecmwf_file}', a_filename , exe)
        
        command = '%s' % (exe)
        
        print('will run [%s]\n' % (command) )
        
        # call the command
        retcode = call(command, shell=True)
        
        print("retcode %s\n" %(retcode) )
        
        if retcode != 0:
            raise Exception("Cannot run g2s for %s. Check error in %s"%(a_filename, log_file))
        
        print("G2S bin file %s/%s generated \n" % (a_output_dir, bin_file) )
        
    else:
        print("G2S bin file %s/%s previously generated \n" % (a_output_dir, bin_file) )

    return '%s/%s' %(a_output_dir, bin_file)

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

def call_g2s_client(a_netcdf_dir, a_file_path, a_ecmwf_path, a_lats, a_lons, a_sta_names):
    """  call g2s_client """
    conf = Conf.get_instance()
    
    lib_g2s_path = conf.get('G2SCLIENT','lib_g2s')
    
    # get nb of altitude values
    nz = conf.getint('G2SCLIENT', 'nb_levels', 401)
    dz = conf.getfloat('G2SCLIENT', 'level_step', 0.5)

    libg2s = cdll.LoadLibrary(lib_g2s_path)
    
    print("libg2s = %s\n" % (libg2s) )
    
    
    
    # call the g2sclient
    g2sclient_pt = libg2s.g2sclient_pt
    
    err = -1
    pt_err = byref(c_int(err))
    
    nb_points = len(a_lats)
    
    pt_nb_points = byref(c_int(nb_points))
    
    # Prepare type double * nb of lat points
    lat_arr = c_double * nb_points
    lon_arr = c_double * nb_points
    
    # allocate and add values (lat=10 and lon=10)
    lat_points = lat_arr()
    lon_points = lon_arr()
    
    for i in xrange(0, nb_points):
        lat_points[i] = a_lats[i]
        lon_points[i] = a_lons[i]
    
    pt_nz = byref(c_int(nz))
    
    pt_dz = byref(c_double(dz))
    #command  = 'extract'
    # need to pad with space chars the command string
    command  = string.ljust('extract', 128)
    pt_command  = c_char_p(command)
    
    filename = string.ljust(a_file_path, 128)
    
    # check if filename exist otherwise error
    if not os.path.exists(filename):
        print("Error the G2S binary file cannot be found %s\n" %(filename))
        return err
        
    pt_filename = c_char_p(filename)
    
    # add datetime
    dt = get_datetime_from_ecmwf_file_name(a_ecmwf_path)
    
    # create the 3 array types
    dim = nb_points * nz
    
    cz_t = c_double * dim
    uz_t = c_double * dim
    vz_t = c_double * dim
    
    cz = cz_t()
    uz = uz_t()
    vz = vz_t()
    
    print("Calling g2sclient_pt")
    #g2sclient_pt(pt_err,lat_points, lon_points, pt_nb_points, pt_filename, pt_command, pt_nz, pt_dz, cz, uz, vz)
    
    time_spent = ftimer(g2sclient_pt, [pt_err,lat_points, lon_points, pt_nb_points, pt_filename, pt_command, pt_nz, pt_dz, cz, uz, vz], {})
    
    print("Run g2sclient in %.2f sec\n" %(time_spent))
      
    # the fortran program returns if we have 2 points and 3 lev
    # (pt1,lev1),(pt2,lev1),(pt1,lev2),(pt2,lev2),(pt1,lev3),(pt2,lev3)
    # so we need to reshape dim1=nz (3) dim= nb_points (2):
    #   
    #  (pt1,lev3),(pt2,lev3)
    #  (pt1,lev2),(pt2,lev2)
    #  (pt1,lev1),(pt2,lev1)
    # we can then transpose the axes to obtain
    #  (pt2,lev1),(pt2,lev2),(pt2,lev3)
    #  (pt1,lev1),(pt1,lev2),(pt1,lev3)
    
    # try to reshape
    cz = numpy.reshape(cz,(nz,nb_points))
    cz = numpy.transpose(cz)
    
    uz = numpy.reshape(uz,(nz,nb_points))
    uz = numpy.transpose(uz)
    
    vz = numpy.reshape(vz,(nz,nb_points))
    vz = numpy.transpose(vz)
    
    #for pt in range(nb_points):
    #    for lev in range(nz):
    #        print("pt_ind=%s,lev_ind=%s,celerity=%s\n" %(pt, lev, cz[pt][lev]))
    
    err = create_netcdf('%s/G2SECMWF_%s_STA.nc' % (a_netcdf_dir, dt.strftime('%y%m%d%H') ), \
                         lat_points, lon_points, nz, cz, uz, vz, dt, a_sta_names)
    
    return err

def create_netcdf(a_netcdf_filename, a_lat_points, a_lon_points, a_nb_levels, a_celerity_arr, a_u_arr, a_v_arr, a_time, a_loc_names):
    """
    dimensions:
      altitude = 401;
      profile  = 1 ;

    variables:
       float altitude(altitude) ;
         altitude:long_name = "height above mean sea level" ;
         altitude:units = "km" ;
         altitude:positive = "up" ; 

       double time(profile);
         time:long_name = "time" ;
         time:units = "days since 1970-01-01 00:00:00" ;
    
       string loc_name(profile) ;
        loc_name:units = "-" ;
        loc_name:long_name = "Location name" ;

       float lon(profile);
         lon:long_name = "longitude" ;
         lon:units = "degrees_east" ;

       float lat(profile);
         lat:long_name = "latitude" ;
         lat:units = "degrees_north" ;

       float celerity(profile, altitude) ;
         celerity:long_name = "celerity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;

       float u(profile, altitude) ;
         u:long_name = "U velocity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;

       float v(profile, altitude) ;
         u:long_name = "V velocity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;
   
       attributes:
          :CF\:featureType = "profile";
 

    """
    print("In create_netcdf %s" %(a_netcdf_filename))
    
    conf = Conf.get_instance()
    
    netcdf_format  = conf.get('NETCDF', 'produced_format', 'NETCDF3_CLASSIC')
    
    #create file
    dataset = Dataset(a_netcdf_filename, 'w', format=netcdf_format)
    
    #create dimension
    dataset.createDimension('altitude', a_nb_levels)
    dataset.createDimension('profile', len(a_lat_points))
    loc_name_len = dataset.createDimension('loc_name_len', 5)

    #create basic variables
    the_time  = dataset.createVariable('time',      'f8', ('profile'))
    lat       = dataset.createVariable('latitude',  'f4', ('profile'))
    lon       = dataset.createVariable('longitude', 'f4', ('profile'))
    altitudes = dataset.createVariable('altitude',  'f4', ('altitude'))

    # create loc_name
    # In netcdf4 it would be 
    #loc_names  = dataset.createVariable('loc_name', str,('profile'))
    if netcdf_format == 'NETCDF3_CLASSIC':
        loc_names  = dataset.createVariable('loc_name', 'c', ('profile','loc_name_len') )
    else:
        loc_names  = dataset.createVariable('loc_name', str, ('profile') )
 
 
    # create param variables
    # u and v wind components
    u         = dataset.createVariable('u',   'f4', ('profile', 'altitude'))
    v         = dataset.createVariable('v',   'f4', ('profile', 'altitude'))
    # celerity 
    c         = dataset.createVariable('c',    'f4', ('profile','altitude'))

    #dataset.sync()

    # add attributes
    dataset.description = 'CTBTO Infrasound wind profiles'
    dataset.history     = 'Created ' + time.ctime(time.time()) + ' by infra-profile-generator-v1.2.2'
    dataset.source      = 'infra-profile-generator-v1.2.2'
    dataset.version     = 'infrasound profile v1.0-20090801'
    #dataset.station     = 'IS42'
    lat.units           = 'degrees north'
    lat.long_name       = 'Latitude'
    lon.units           = 'degrees east'
    lon.long_name       = 'Longitude'
    altitudes.units     = 'm'
    altitudes.long_name = 'Altitude'
    loc_names.units     = '-'
    loc_names.long_name = 'Location name'
    the_time.units      = 'hours since 1970-01-01 00:00:00.0'
    the_time.calendar   = 'gregorian'
    the_time.long_name  = 'Time'
    # param attributes
    u.units             = 'm s**-1'
    u.long_name         = 'U velocity'
    v.units             = 'm s**-1'
    v.long_name         = 'V velocity'
    c.units             = 'm s**-1'
    c.long_name         = 'Celerity'

    # create altitude
    alts = numpy.arange(0, 500*a_nb_levels, 500)

    altitudes[:] = alts

    # add lat,lon
    lat[:]    = a_lat_points
    lon[:]    = a_lon_points
    #not used for the moment
    
    print("a_loc_names %s\n" % (a_loc_names))
    
    
    if netcdf_format == 'NETCDF3_CLASSIC':
        # NETCDF3 CLASSIC doesn't know about str
        cpt = 0
        for name in a_loc_names:
            loc_names[cpt] = stringtoarr(name,len(loc_name_len))
            cpt += 1
    else:
        # NETCDF4
        cpt = 0
        for name in a_loc_names:
            loc_names[cpt] = name
            cpt += 1
    
    #add time
    dt  = date2num(a_time, "days since 1970-01-01 00:00:00", calendar = 'gregorian') 
    
    #create the time array
    data_time = numpy.repeat(dt, len(a_lat_points) )

    the_time[:] = data_time
    dataset.sync()

    c[:]=a_celerity_arr[:]
    u[:]=a_u_arr[:]
    v[:]=a_v_arr[:]

    dataset.sync()

    dataset.close()

    return 0

def do_run(path, args, lats, lons, sta_names):
    """ do run """
    print("===================================================================\n")
           
    print("Generation for %s \n" %(path) )
        
    (f107, f107a, ap) = get_noaa_indices(path)
    
    bin_file_path = run_g2s(args['bin_dir'], path, f107, f107a, ap)
    
    print("bin_file_path %s\n" %(bin_file_path))
    
    call_g2s_client(args['netcdf_dir'],bin_file_path, path, lats, lons, sta_names)
            
    print("===================================================================\n")
      
if __name__ == "__main__":
    
    
    try:
        args = {}
        
        load_configuration(args)
        
        args = parse_arguments(sys.argv[1:])
        
        ecmwf_data_paths = get_ecmwf_data(args['start'], args['end'])
        
        print("BIN files written in %s\n" % (args['bin_dir']) )
        print("netcdf files written in %s\n" %(args['netcdf_dir']) )                                
        
        print("Ecmwf data paths %s\n" %(ecmwf_data_paths))
        
        (sta_names, lats, lons) = _get_station_info()
    
        for path in ecmwf_data_paths:
            time_spent = ftimer(do_run, [path, args, lats, lons, sta_names], {})
            
            print("Generation for %s done in %.2f seconds \n" %(path, time_spent) )
        
    except ParsingError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error()))
        usage() 
        sys.exit(2)
    except ConfAccessError, e:
        # Not Runner set print
        print("Error - %s"%(e.get_message_error())) 
        if args.get('verbose', 1) == 3:
            print("Traceback: %s."%(get_exception_traceback()))
        usage() 
        sys.exit(2)
        
        
        

        
        
    
    