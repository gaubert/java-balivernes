#!/usr/bin/python
'''
Created on Jun 17, 2009

@author: guillaume.aubert@ctbto.org
'''

import os
import re
import csv
import getopt, sys

PATTERN  = "[\w\d]+_\Day\d\d_\d*_DPRK2\.txt$"
    
FILES_RE = re.compile(PATTERN, re.IGNORECASE)

def run(a_args):
    """ start by reading the dir """
    
    the_dir = a_args['dir']
    
    print ("Try to read files under %s\n" % (the_dir) )
    
    files = os.listdir(the_dir)       
    
    files = [f for f in files if FILES_RE.search(f)]
    
    if len(files) == 0:
        print ('No files found in %s with the matching pattern %s\n' % (dir, PATTERN))
    
    the_matrix = {}
    
    for file_path in files:
        print("Compute average values for file %s" % ('%s/%s' % (the_dir, file_path)))
        the_split = file_path.split('_')
        the_matrix['%s_%s' % (the_split[1], the_split[2])] = compute_average(read_file('%s/%s' % (the_dir, file_path)))
     
     
    sorted_keys = the_matrix.keys()
    sorted_keys.sort()
    
    print("\nWrite values in %s" % (a_args['output']))
    
    wri_csv = csv.writer(open(a_args['output'],'w'), delimiter=',')
    
    header_written = False
    #get complete list of available dates from day2
    all_dates = the_matrix[sorted_keys[0]].keys()
    
    rows = []
    
    for day in sorted_keys:
        
        local_dates = the_matrix[day].keys()
        
        all_dates = list( set(all_dates) | set(local_dates) )
        all_dates.sort()
        
        row = []
        #add row header
        row.append(day)
        
        for date in all_dates:
            
            val = the_matrix[day].get(date, None)
            if val is not None:
                row.append(val)
            else:
                row.append(' ')
        
        #print "%s : %s\n" % (day, row)
        
        rows.append(row)
        
    #print "Matrix %s\n" %(the_matrix)
    
    #add column header
    if not header_written:
        header_written = True
        lis = [' ']
        lis.extend(all_dates)
        wri_csv.writerow(lis)
    
    for row in rows:
        wri_csv.writerow(row)
                                                
    return the_matrix
        
        
def read_file(a_file):
    """ read a file """
    fdesc = open(a_file)
    
    data  = {}
    
    for line in fdesc.readlines():
        
        fields = line.split(' ')
        
        key = fields[0]
        #sensitivity
        val = float(fields[4])
        
        if key in data:
            data[key].append(val)
        else:
            data[key] = [ val ]
    
    return data
    

def compute_average(a_data):
    """ compute average from list """
    
    result = {}
    
    for key, val_list in a_data.items():
        average = float(sum(val_list)) / len(val_list)
        result[key] = average
    
    return result

def usage():
    
    usage_string = """
Usage: sensitivity_extractor [options] 

  Mandatory Options:
  --dir           (-d)    dir containing the samples for one unique station
                         

  Extra Options:
  --output        (-o)    output path  (default=/tmp/output.csv)
                          
  Help Options:
   --help     Show this usage information.

  Examples:
  >./sensitivity_extractor --output /tmp/JPX38_results.csv --dir /tmp/JPX38
 
  """
       
    print(usage_string)
    
NAME        = "sens_extractor"
VERSION     = "1.0"

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
    result['dir']                   = None
    result['output']                = '/tmp/results.csv'
    
    try:
        (opts, _) = getopt.gnu_getopt(a_args, "hd:o:v", ["help", "dir=", "output=", "version"])
    except Exception, err: #IGNORE:W0703
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-v":
            print("%s v %s"%(NAME, VERSION))
            sys.exit()
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--dir"):
            result['dir'] = arg
        elif opt in ("-o", "--output"):
            result['output'] = arg
        else:
            raise Exception("Unknown option %s = %s"%(opt, arg))
    
    # missing parameters
    if result['dir'] is None:
        print ("Error: Missing --dir option")
        usage()
        sys.exit(2)
            
    return result
        

if __name__ == '__main__':
    
    args = parse_arguments(sys.argv[1:])
    
    run(args)