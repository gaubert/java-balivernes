import datetime
import subprocess
import ctbto.common.utils


def copy_data(begin_date,end_date):
    
    root_dir = "/tmp/copy-data"
    
    ctbto.common.utils.makedirs(root_dir)
    
    begin = datetime.datetime.strptime(begin_date,'%Y-%m-%d')
    end   = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    
    current = begin
    
    processed = "/home/misc/rmsops/data/processed"
    
    # List of dir where to fetch data
    #internal_dirs = ["alert","blank","cal","detbk","flow","gasbk","met","qc","rlr","sample","soh"]
    # remove met, flow, rlr for the moment
    internal_dirs = ["alert","blank","cal","detbk","flow","gasbk","qc","sample","soh"]
    
    while current <= end:
        
        current_time_tuple = current.timetuple()   
        current_day_num = current_time_tuple[7]
        current_year    = current_time_tuple[0]
    
        for i_d in internal_dirs:
        
            # add year
            path = "%s/%s/%s"%(processed,i_d,current_year)
        
            print("**************************************************\n")
            print("Retrieve all data in %s\n"%(path))
    
            command = ""
    
            # create root dir if it doesn't exists
            orig_path_dir = "%s/%s"%(path,current_day_num)
         
            dest_path_dir = "%s/%s"%(root_dir,orig_path_dir)
         
            ctbto.common.utils.makedirs(dest_path_dir)
         
            command = "/usr/bin/scp -r aubert@kuredu:%s/* %s"%(orig_path_dir,dest_path_dir)
    
            print "execute %s\n"%(command)
        
            tries = 1
        
            while tries < 2:
    
                res = subprocess.call(command,shell=True)
            
                if res != 0:
                    print("Error when executing %s. See log files.\n"%(command))
                
                tries += 1
                
        current = current + datetime.timedelta(1)

def copy_reports(begin_date,end_date):
    
    root_dir = "/tmp/copy-data"
    
    ctbto.common.utils.makedirs(root_dir)
    
    begin = datetime.datetime.strptime(begin_date,'%Y-%m-%d')
    end   = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    
    current = begin
    
    products = ["/home/misc/rmsops/products/rrr","/home/misc/rmsops/products/arr","/home/misc/rmsops/products/ssreb","/home/misc/rmsops/data/spectrum"]
    
    while current <= end:
        
        date_dir = current.strftime('%y_%b_%d').lower()
      
        print "dir = %s\n"%(date_dir)
        
        for path in products:
            
            orig_path_dir = "%s/%s"%(path,date_dir)
            
            dest_path_dir = "%s/%s"%(root_dir,orig_path_dir)
            
            ctbto.common.utils.makedirs(dest_path_dir)
            
            command = "/usr/bin/scp -r aubert@kuredu:%s/* %s"%(orig_path_dir,dest_path_dir)
    
            print "execute %s\n"%(command)
        
            tries = 1
        
            while tries < 2:
    
                res = subprocess.call(command,shell=True)
            
                if res != 0:
                    print("Error when executing %s. See log files.\n"%(command))
                
                tries += 1
        
        current = current + datetime.timedelta(1)
    
    
    
         

if __name__ == '__main__':
    
    copy_data('2008-10-01','2008-10-15')
    
    copy_reports('2008-10-01','2008-10-15')
   
   