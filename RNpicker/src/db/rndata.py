r""" Return object for access the Radionuclide data locally or remotely 

"""

import logging
import os
import subprocess
import common.utils
import common.exceptions

__all__ = ["RemoteFSDataSource"]

def _complain_ifclosed(closed):
    if closed:
        raise ValueError, "I/O operation on closed file"

class RemoteFSDataSource:
    """ get data from the a remote filesystem using ssh.
        fetch remote file and open a file descriptor on the local file
        and delegate all methods to the open file
        
            Args:
               aFilePath
        
            Returns:
              the built hashtable
              
            Raises:
               exception
    """
    
     # Class members
    c_log = logging.getLogger("rndata.RemoteFileSystemDataSource")
    c_log.setLevel(logging.DEBUG)
    
    def _getRemoteFile(self):
        """ fetch the file and store it in a temporary location """
        
        # no local filename so use the remote file basename
        if self._localFilename is None:
            self._localFilename = os.path.basename(self._remotePath)
        
        # make local dir if not done
        common.utils.makedirs(self._localDir)
            
        # path under which the file is going to be stored
        destinationPath = "%s/%s"%(self._localDir,self._localFilename)
        
        # if file there and caching activated open fd and quit
        if os.path.exists(destinationPath) and self._cachingActivated:
            self._fd = open("%s/%s"%(self._localDir,self._localFilename),"r")
            return
        
        res = subprocess.call([self._remoteScript,self._remotePath,destinationPath])
        if res != 0:
           raise common.exceptions.CTBTOError(-1,"Error when executing sftp Script %s\n"%(self._remoteScript))
        
        self._fd = open("%s/%s"%(self._localDir,self._localFilename),"r")
    
    def __init__(self, aDataPath):
        
        self.len = 0
        self.buflist = []
        self.pos = 0
        self.closed = False
        self.softspace = 0
        
        # my variables
         
        # get reference to the conf object
        self._conf              = common.utils.Conf.get_conf()
        
        self._remotePath        = aDataPath
        
        self._remoteScript      = self._conf.get("RemoteAccess","sftpScript")
        
        self._localDir          = self._conf.get("RemoteAccess","localDir")
        
        self._cachingActivated  = self._conf.getboolean("RemoteAccess","cachingActivated") if self._conf.has_option("RemoteAccess","cachingActivated") else False
        
        self._localFilename     = self._conf.get("RemoteAccess","localFilename") if self._conf.has_option("RemoteAccess","localFilename") else None
        
        self._fd                 = None
        
        self._getRemoteFile()
        

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

# A little test suite

def test():
    import sys
    if sys.argv[1:]:
        file = sys.argv[1]
    else:
        file = '/etc/passwd'
    lines = open(file, 'r').readlines()
    text = open(file, 'r').read()
    f = StringIO()
    for line in lines[:-2]:
        f.write(line)
    f.writelines(lines[-2:])
    if f.getvalue() != text:
        raise RuntimeError, 'write failed'
    length = f.tell()
    print 'File length =', length
    f.seek(len(lines[0]))
    f.write(lines[1])
    f.seek(0)
    print 'First line =', repr(f.readline())
    print 'Position =', f.tell()
    line = f.readline()
    print 'Second line =', repr(line)
    f.seek(-len(line), 1)
    line2 = f.read(len(line))
    if line != line2:
        raise RuntimeError, 'bad result after seek back'
    f.seek(len(line2), 1)
    list = f.readlines()
    line = list[-1]
    f.seek(f.tell() - len(line))
    line2 = f.read()
    if line != line2:
        raise RuntimeError, 'bad result after seek back from EOF'
    print 'Read', len(list), 'more lines'
    print 'File length =', f.tell()
    if f.tell() != length:
        raise RuntimeError, 'bad length'
    f.truncate(length/2)
    f.seek(0, 2)
    print 'Truncated length =', f.tell()
    if f.tell() != length/2:
        raise RuntimeError, 'truncate did not adjust length'
    f.close()