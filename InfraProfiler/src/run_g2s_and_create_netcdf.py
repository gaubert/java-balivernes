'''
Created on Sep 1, 2009

@author: guillalume.aubert@ctbto.org
'''
# common packages
import os
import datetime
import fnmatch
import re
import cStringIO
from   subprocess import Popen, PIPE, STDOUT

from org.ctbto.conf import Conf

class CLIError(Exception):
    """ Base class exception """
    pass

class FindError(CLIError):
    """ find error """

    def __init__(self, a_error_msg):
        super(FindError,self).__init__()
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

def ffind(path, shellglobs=None, namefs=None, relative=True):
    """
    Finds files in the directory tree starting at 'path' (filtered by
    Unix shell-style wildcards ('shellglobs') and/or the functions in
    the 'namefs' sequence).

    The parameters are as follows:

    - path: starting path of the directory tree to be searched
    - shellglobs: an optional sequence of Unix shell-style wildcards
      that are to be applied to the file *names* found
    - namefs: an optional sequence of functions to be applied to the
      file *paths* found
    - relative: a boolean flag that determines whether absolute or
      relative paths should be returned

    Please not that the shell wildcards work in a cumulative fashion
    i.e. each of them is applied to the full set of file *names* found.

    Conversely, all the functions in 'namefs'
        * only get to see the output of their respective predecessor
          function in the sequence (with the obvious exception of the
          first function)
        * are applied to the full file *path* (whereas the shell-style
          wildcards are only applied to the file *names*)

    Returns a sequence of paths for files found.
    """
    if not os.access(path, os.R_OK):
        raise FindError("cannot access path: '%s'" % path)

    fileList = [] # result list
    try:
        for dir, subdirs, files in os.walk(path):
            if shellglobs:
                matched = []
                for pattern in shellglobs:
                    filterf = lambda s: fnmatch.fnmatchcase(s, pattern)
                    matched.extend(filter(filterf, files))
                fileList.extend(['%s%s%s' % (dir, os.sep, f) for f in matched])
            else:
                fileList.extend(['%s%s%s' % (dir, os.sep, f) for f in files])
        if not relative: fileList = map(os.path.abspath, fileList)
        if namefs: 
            for ff in namefs: fileList = filter(ff, fileList)
    except Exception, e: raise FindError(str(e))
    return(fileList)

    
    
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
        os.environ[Conf.ENVNAME] = '%s/%s'%(conf_dir, 'infra_profiler.config')
        
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
    result = []
    
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
    
    
    start = get_datetime_from_str(a_start)
    
    end   = get_datetime_from_str(a_end)
    
    filenames = build_list_of_filenames(start,end)
    
    print('filenames = %s\n' % (filenames) )
    
    conf = Conf.get_instance()
    
    prod_dir = conf.get('ECMWFDATA', 'production_loc')
    arch_dir = conf.get('ECMWFDATA', 'archive_loc')
    
    prod_list = []
    arch_list = []
    
    # best effort policy try to get all possible files
    try:
        prod_list = get_files_from(prod_dir, filenames)
    except Exception, e:
        print("Warning. Error: %s\n" %(e) )
        
    """try:
        arch_list = get_files_from(arch_dir, filenames)
    except Exception, e:
        print("Warning. Error: %s\n" %(e) )
    """
    
    print('files found in prod %s\n' %(prod_list) )
    print('files found in arch %s\n' %(arch_list) )

    result.extend(prod_list)
    result.extend(arch_list)
    
    return result

def get_noaa_indices(a_ecmwf_file_name):
    """
       get noaa indices for a particular date.
       This calls a scripts that gets the data from NOAA web site
       
       Args:
          a_ecmwf_file_name : ecmwf file name starting with EN
    """
    
    # create a datetime from the ECMWF filename and convert it in NOAA form '%Y%m%d'
    str_date = os.path.basename(a_ecmwf_file_name)
    str_date = str_date[2:]
    
    the_date =datetime.datetime.strptime(str_date, '%y%m%d%H')
    
    noaa_date = the_date.strftime('%Y%m%d')
    
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
        fh = cStringIO.StringIO(stdout)
        
        f107  = ""
        f107a = ""
        ap    = ""
        
        cpt = 0
        for line in fh:
            print ("line = %s\n" % (line) )
            if cpt == 0:
                f107 = line.strip()
            elif cpt == 1:
                f107a = line.strip()
            elif cpt == 2:
                ap = line.strip()
            cpt += 1
        
        print("All = %s,%s,%s\n" %(f107, f107a, ap))
        return (f107, f107a, ap)
 

            

if __name__ == "__main__":
    
    args = {}
    
    load_configuration(args)
    
    ecmwf_data_paths = get_ecmwf_data("2009-07-01T03", "2009-08-31T15")
    
    print("Ecmwf data paths %s\n" %(ecmwf_data_paths))
    
    f107  = None
    f107a = None
    ap    = None
        
    
    for path in ecmwf_data_paths:
        #(f107, f107a, ap) = get_noaa_indices(path)
        result = get_noaa_indices(path)
        print('result = %s\n' % (result))
        
        
    
    