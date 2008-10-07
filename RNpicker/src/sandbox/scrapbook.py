from StringIO import StringIO
import operator
import string
import subprocess
import base64
import os
import zlib
import distutils.dir_util
import common.utils

from db.rndata import RemoteFSDataSource
 
#
str1 = """Dallas Cowboys football practice at Valley Ranch was delayed on Wednesday
#
for nearly two hours. One of the players, while on his way to the locker
#
room happened to look down and notice a suspicious looking, unknown white
#
powdery substance on the practice field.
#
 
#
The coaching staff immediately suspended practice while the FBI was
#
called in to investigate. After a complete field analysis, the FBI
#
determined that the white substance unknown to the players was the goal
#
line.
#
 
#
Practice was resumed when FBI Special Agents decided that the team would not
#
be likely to encounter the substance again.
#
"""

def f(a,b):
    
    return a+b

class curry:
    
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()
    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.fun(*(self.pending + args), **kw)

def testCurrying():
    
   double = curry(string.ljust,width=20)

   res = double("totototo")
   
   print "Res [%s]\n"%(res)
   
   list = ['4          ', '6          ', '3          ', '2          ', '5          ']

def testsubProcess():
    
    res = subprocess.call(["/home/aubert/sftpTest.sh","08_sep_01"])
    
    #res = subprocess.call(["ls","-la"])
    
    print "res=%d\n"%(res)

def testCompress():
    
   zstr1 = zlib.compress(str1)
 
   print "Length of zipped str1 =", len(zstr1)
   
   uncompressed = zlib.decompress(zstr1)
   
   print "Lenght of unzipped str1 = ",len(uncompressed)
   
   s = base64.b64encode("ADDDDDD")

def testRemoteDataSource(self):
    
    l = "/tmp/toto/titi/t.tmp"
    
    print "basename = %s\n"%(os.path.basename(l))
    
    
    input = RemoteFSDataSource("/ops/data/rn/spectrum/08_aug_14/fjp26_001_882731g.s")
    
    for line in input:
        print "the line = %s\n"%(line)

def makedirrs(name):
  head, tail = os.path.split(name)
  if not tail:
    head, tail = os.path.split(head)
  if head and tail and not os.path.exists(head):
    makedirs(head)
  try:
    os.mkdir(name)
  except EnvironmentError:
    if not os.path.isdir(name):
      raise


if __name__ == '__main__':
    
    #distutils.dir_util.mkpath("/tmp/totoo",verbose=1)
    
    common.utils.makedirs("/tmp/tata/r")
    
    print "Hello \n"
    
    
   
  
   
