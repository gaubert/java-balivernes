

import subprocess
import os
import logging
import logging.handlers
import ctbto.tests
import ctbto.common.utils
import ctbto.db.rndata
from   ctbto.common.utils import ftimer
from   org.ctbto.conf  import Conf


def get_list_messages_to_copy(a_script,a_hostname,a_origin_dir,a_local_dir,a_remote_user='aubert',a_result_file='result.msgs'):
    
    # make local dir if not done
    ctbto.common.utils.makedirs(a_local_dir)
            
    # path under which the file is going to be stored
    destinationPath = "%s/%s"%(a_local_dir,a_result_file)

    func = subprocess.call
      
    res   = []  
              
    t = ftimer(func,[[a_script,a_hostname,a_origin_dir,destinationPath,a_remote_user]],{},res,number=1)
    
    print("\nCreated file: %s in %s secs \n /n"%(destinationPath,t))
    
    if res[0] != 0:
        raise Exception(-1,"Trying to fetch remote file (using ssh) with\"%s %s %s %s %s. Error code %s\n"%(a_script,a_hostname,a_origin_dir,destinationPath,a_remote_user,res[0]) )
    
    return open(destinationPath)

def _get_tests_dir_path():
    """ get the ctbto.tests path depending on where it is defined """
        
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
        hdlr.setFormatter(fmt)
        console.setFormatter(fmt)
        logging.root.addHandler(hdlr)
        logging.root.addHandler(console)
        
        log = logging.getLogger("ROOT")
        log.setLevel(logging.INFO)
        log.info("Start")
        
def main():
    
    myBasicLoggingConfig()
     
    os.environ['RNPICKER_CONF_DIR'] = _get_tests_dir_path()
        
    os.environ[Conf.ENVNAME] = '%s/%s'%(_get_tests_dir_path(),'rnpicker.config')
        
    # create an empty shell Conf object
    conf = Conf.get_instance()
    
    local_dir = '/tmp/req_messages'
    # cheat and always ask for 5 MB
    remote_file_size =5 * 1024 * 1024
    
    fd = get_list_messages_to_copy(conf.get("RemoteAccess","getRequestMessage"), conf.get("RemoteAccess","devlanAccessHost"),"/ops/data/shared/messages/2009/131",local_dir,conf.get("RemoteAccess","devlanAccessUser"))
    #fd = open('/tmp/req_messages/result.msgs','r')

    cpt = 0
    for line in fd:
        print "line = %s\n"%(line)
        filename = os.path.basename(line.strip())
       
        # this will automatically write the file in the destination dir as there is some caching
        theInput = ctbto.db.rndata.RemoteArchiveDataSource(aDataPath = line.strip(),aID = cpt,aRemoteOffset = 0,aRemoteSize = remote_file_size,aRemoteHostname=conf.get("RemoteAccess","devlanAccessHost"),aRemoteScript=conf.get("RemoteAccess","archiveAccessScript"),aRemoteUser=conf.get("RemoteAccess","devlanAccessUser"),aLocalDir=local_dir,a_DoNotUseCache=False,a_LocalFilename=filename)
        
        #writer = open('/tmp/req_messages/%s'%(filename),'w')
        
        #for data in theInput:
        #   writer.write(data)
        
        #writer.close()
        
        cpt += 1


if __name__ == "__main__":
    main()