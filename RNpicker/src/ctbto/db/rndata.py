r""" Return object for access the Radionuclide data locally or remotely 

"""

import logging
import os
import subprocess

import ctbto.common.utils
from ctbto.common.utils import ftimer
from ctbto.common import CTBTOError
from org.ctbto.conf import Conf

def _complain_ifclosed(closed):
    if closed:
        raise ValueError, "I/O operation on closed file"
    
class BaseRemoteDataSource(object):
    """ Base class for All Remote Sources
    """
    
    # Class members
    c_log = logging.getLogger("rndata.BaseRemoteDataSource")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self, aDataPath,aID,aRemoteOffset,aRemoteSize):
        
        self.len = 0
        self.buflist = []
        self.pos = 0
        self.closed = False
        self.softspace = 0
        
        # my variables
         
        # get reference to the conf object
        self._conf              = Conf.get_instance()
        
        self._remotePath        = aDataPath
        
        self._id                = aID
        
        self._localDir          = self._conf.get("RemoteAccess","localDir")
        
        self._cachingActivated  = self._conf.getboolean("RemoteAccess","cachingActivated",False)
        
        self._localFilename     = self._conf.get("RemoteAccess","localFilename") if self._conf.has_option("RemoteAccess","localFilename") else None
        
        self._fd                = None
        
        # these two options are only read in the ArchiveDataSource for the moment.
        # This should be generalized to all Files and the hierachy might disapear ?
        
        # where to point in the file
        self._remoteOffset      = aRemoteOffset
        
        # Size to read 
        self._remoteSize        = aRemoteSize
        
    def getLocalFilename(self):
        """ localFilename Accessor """
        
        return self._localFilename
        
        
    def _getRemoteFile(self):
        """ abstract global data fetching method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    

    def __iter__(self):
        return self

    def next(self):
        """A file object is its own iterator, for example iter(f) returns f
        (unless f is closed). When a file is used as an iterator, typically
        in a for loop (for example, for line in f: print line), the next()
        method is called repeatedly. This method returns the next input line,
        or raises StopIteration when EOF is hit.
        """
        _complain_ifclosed(self.closed)
        return self._fd.next()

    def close(self):
        """Free the memory buffer.
        """
        if not self.closed:
            self._fd.close()
            self.closed = True
            

    def isatty(self):
        """Returns False because StringIO objects are not connected to a
        tty-like device.
        """
        _complain_ifclosed(self.closed)
        return False

    def seek(self, pos, mode = 0):
        """Set the file's current position.

        The mode argument is optional and defaults to 0 (absolute file
        positioning); other values are 1 (seek relative to the current
        position) and 2 (seek relative to the file's end).

        There is no return value.
        """
        _complain_ifclosed(self.closed)
        self._fd.seek(pos,mode)

    def tell(self):
        """Return the file's current position."""
        _complain_ifclosed(self.closed)
        return self._fd.tell()

    def read(self, n = -1):
        """Read at most size bytes from the file
        (less if the read hits EOF before obtaining size bytes).

        If the size argument is negative or omitted, read all data until EOF
        is reached. The bytes are returned as a string object. An empty
        string is returned when EOF is encountered immediately.
        """
        _complain_ifclosed(self.closed)
        return self._fd.read(n)

    def readline(self, length=None):
        r"""Read one entire line from the file.

        A trailing newline character is kept in the string (but may be absent
        when a file ends with an incomplete line). If the size argument is
        present and non-negative, it is a maximum byte count (including the
        trailing newline) and an incomplete line may be returned.

        An empty string is returned only when EOF is encountered immediately.

        Note: Unlike stdio's fgets(), the returned string contains null
        characters ('\0') if they occurred in the input.
        """
        _complain_ifclosed(self.closed)
        return self._fd.readline(length)

    def readlines(self, sizehint = 0):
        """Read until EOF using readline() and return a list containing the
        lines thus read.

        If the optional sizehint argument is present, instead of reading up
        to EOF, whole lines totalling approximately sizehint bytes (or more
        to accommodate a final whole line).
        """
        return self._fd.readlines(sizehint)

    def truncate(self, size=None):
        """Truncate the file's size.

        If the optional size argument is present, the file is truncated to
        (at most) that size. The size defaults to the current position.
        The current file position is not changed unless the position
        is beyond the new file size.

        If the specified size exceeds the file's current size, the
        file remains unchanged.
        """
        _complain_ifclosed(self.closed)
        self._fd.truncate(size)

    def write(self, s):
        """Write a string to the file.

        There is no return value.
        """
        _complain_ifclosed(self.closed)
        self._fd.write(s)

    def writelines(self, iterable):
        """Write a sequence of strings to the file. The sequence can be any
        iterable object producing strings, typically a list of strings. There
        is no return value.

        (The name is intended to match readlines(); writelines() does not add
        line separators.)
        """
        self._fd.writelines(iterable)

    def flush(self):
        """Flush the internal buffer
        """
        _complain_ifclosed(self.closed)
        self._fd.flush()

class RemoteFSDataSource(BaseRemoteDataSource):
    """ get data from the a remote filesystem using ssh.
        fetch remote file and open a file descriptor on the local file
        and delegate all methods to the open file
    """
    
    # Class members
    c_log = logging.getLogger("rndata.RemoteFileSystemDataSource")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self, aDataPath,aID,aOffset,aSize):
        
        super(RemoteFSDataSource,self).__init__(aDataPath,aID,aOffset,aSize)
        
        self._remoteScript      = self._conf.get("RemoteAccess","prodAccessScript")
        
        self._remoteHostname    = self._conf.get("RemoteAccess","prodAccessHost")
        
        self._remoteUser        = self._conf.get("RemoteAccess","prodAccessUser")
        
        self._getRemoteFile()
        
    
    def _getRemoteFile(self):
        """ fetch the file and store it in a temporary location """
        
        # no local filename so use the remote file basename
        if self._localFilename is None:
            self._localFilename = os.path.basename(self._remotePath)
        
        # make local dir if not done
        ctbto.common.utils.makedirs(self._localDir)
            
        # path under which the file is going to be stored
        destinationPath = "%s/%s"%(self._localDir,self._localFilename)
        
        # if file there and caching activated open fd and quit
        if os.path.exists(destinationPath) and self._cachingActivated:
            self._fd = open(destinationPath,"r")
            return
        
        # try 3 times before to fail
        tries = 1
        res   = []
        
        while tries < 4:
       
            func = subprocess.call
            
            t = ftimer(func,[[self._remoteScript,self._remoteHostname,self._remotePath,str(self._remoteOffset),str(self._remoteSize),destinationPath,self._remoteUser]],{},res,number=1)
       
            RemoteFSDataSource.c_log.info("\nTime: %s secs \n Fetch file: %s on host: %s\n"%(t,self._remotePath,self._remoteHostname))
       
            if res[0] != 0:
                if tries >= 3:
                    raise CTBTOError(-1,"Error when executing remotely script :\"%s %s %s %s %s %s %s\". First Error code = %d\n"%(self._remoteScript,self._remoteHostname,self._remotePath,str(self._remoteOffset),str(self._remoteSize),destinationPath,self._remoteUser,res[0]))
                else:
                    tries += 1
            else:
                tries += 4
              
        self._fd = open(destinationPath,"r")
    
       

class RemoteArchiveDataSource(BaseRemoteDataSource):
    """ get data from the a remote archive filesystem using ssh.
        Go to the given offset, fetch the data and put it locally in a file named
        PATH_SAMPLEID
        
            Args:
               aFilePath
        
            Returns:
              the built hashtable
              
            Raises:
               exception
    """
    
     # Class members
    c_log = logging.getLogger("rndata.RemoteArchiveDataSource")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self, aDataPath,aID,aRemoteOffset,aRemoteSize):
        
        # my variables
        super(RemoteArchiveDataSource,self).__init__(aDataPath,aID,aRemoteOffset,aRemoteSize)
            
        # get reference to the conf object
        self._conf              = Conf.get_instance()
        
        self._remoteScript      = self._conf.get("RemoteAccess","archiveAccessScript")
        
        self._remoteHostname    = self._conf.get("RemoteAccess","archiveAccessHost")
        
        self._remoteUser        = self._conf.get("RemoteAccess","archiveAccessUser")
        
        self._localDir          = self._conf.get("RemoteAccess","localDir")
        
        self._cachingActivated  = self._conf.getboolean("RemoteAccess","cachingActivated") if self._conf.has_option("RemoteAccess","cachingActivated") else False
        
        self._localFilename     = "%s_%s.%s"%(os.path.basename(self._remotePath),self._id,self._getExtension(self._remotePath))
    
        self._getRemoteFile()
        
    def _getExtension(self,aRemotePath):
        """ Find out if this is msg or an extracted spectrum to specify the extension """
        
        # If it contains data then it is msg
        if aRemotePath.find("DATA") != -1:
            return "archmsg"
        elif aRemotePath.find("SPECTHIST") != -1:
            return "archs"
        else:
            RemoteArchiveDataSource.c_log.warning("Warning cannot find the archived file type for %s. Guess it is a message\n"%(aRemotePath))
            return "archmsg"
        
    
    def _getRemoteFile(self):
        """ fetch the file and store it in a temporary location """
        
        # make local dir if not done
        ctbto.common.utils.makedirs(self._localDir)
            
        # path under which the file is going to be stored
        # It is the original filename_id
        # for the moment always assume that it is a spectrum
        destinationPath = "%s/%s"%(self._localDir,self._localFilename)
        
        # if file there and caching activated open fd and quit
        if os.path.exists(destinationPath) and self._cachingActivated:
            self._fd = open(destinationPath,"r")
            return
        
        res  = []
        
        func = subprocess.call
        t = ftimer(func,[[self._remoteScript,self._remoteHostname,self._remotePath,str(self._remoteOffset),str(self._remoteSize),destinationPath,self._remoteUser]],{},res,number=1)
         
        RemoteArchiveDataSource.c_log.info("\nTime: %s secs \n Fetch file: %s on host: %s\n"%(t,self._remotePath,self._remoteHostname))
       
        #res = subprocess.call([self._remoteScript,self._remoteHostname,self._remotePath,str(self._remoteOffset),str(self._remoteSize),destinationPath,self._remoteUser])
        if res[0] != 0:
            raise CTBTOError(-1,"Error when executing remotely script :\"%s %s %s %s %s %s %s\". First Error code = %d\n"%(self._remoteScript,self._remoteHostname,self._remotePath,str(self._remoteOffset),str(self._remoteSize),destinationPath,self._remoteUser,res[0]))
        
        self._fd = open(destinationPath,"r")
    

        

   