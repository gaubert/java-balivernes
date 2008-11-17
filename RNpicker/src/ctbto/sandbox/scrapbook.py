from StringIO import StringIO
import operator
import string
import subprocess
import base64
import os
import zlib
import distutils.dir_util
import ctbto.common.utils
import re



from ctbto.common     import Conf
from ctbto.db.rndata  import RemoteFSDataSource
from ctbto.query      import RequestParser
from ctbto.transformer import XML2HTMLRenderer
 
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

def testRemoteDataSource():
    
    l = "/tmp/toto/titi/t.tmp"
    
    print "basename = %s\n"%(os.path.basename(l))
    
    
    input = RemoteFSDataSource("/ops/data/rn/spectrum/08_aug_14/fjp26_001_882731g.s")
    
    for line in input:
        print "the line = %s\n"%(line)



def testMakedirs():
    
    ctbto.common.utils.makedirs("/tmp/tata/r")
    

def testCheckThatNoTagsAreLeft():
    
    srcMustMatch=""" <Hello firstTag="${_j_j_j_}>
               <T1> ${TAG_2} </T1>
            </Hello>
        """
    
    srcNoMatch=""" <Hello>
               <T1> ${BALDLDLDL </T1>
            </Hello>
        """
    
    pattern="\${\w*}"
    
    res = re.findall(pattern, srcNoMatch)
    
    print "NoMatch =[%s]\n"%(len(res))
    
    res = re.findall(pattern, srcMustMatch)
    
    print "Match =[%s]\n"%(len(res))
    
def testParseSpectrumInfo():
    
    strToParse = "spectrum=PREL/QC/BK"
    
    pattern ="(?P<command>\s*spectrum\s*=\s*)(?P<values>[\w+\s*/\s*]*\w)\s*"
   
    reSpec = re.compile(pattern, re.IGNORECASE)
    
    m = reSpec.match(strToParse)
    
    if m is not None:
      #print "Matooch =[%s],matched=%s\n"%(len(res),res)
      print "command = %s\n"%(m.group('command'))
      
      values = m.group('values')
      
      print "vakues = %s\n"%(values)
      
      vals = values.split('/')
      
      if len(vals) == 0:
          print "There is a problem\n"
        
      for val in vals:
          print "val = %s\n"%(val.strip().upper())

def checksumTest(str):

    chksum = 0L
    toggle = 0

    i = 0
    while i < len(str):
        ch = str[i]
        if ord(ch) > 0:
            if toggle: chksum = chksum << 1
            chksum = chksum + ord(ch)
            chksum = chksum & 0X7fffffff
            toggle = not toggle
        else:
            chksum = chksum + 1
        i = i + 1

    return chksum


def jinja2Test():
    
    filename='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/arr.txt'
    
    # read the full template in a string buffer
    f = open(filename,"r") 
        
    tStr = f.read()
    
    from jinja2 import Template
    from jinja2 import Environment, FileSystemLoader, Undefined
    env = Environment(loader=FileSystemLoader('/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates'))
    
    template = env.get_template('ArrHtml.html')
    
    n_list = [{'name':'xenon-133','half_life':134,'conc':23,'conc_err':2.2},{'name':'xenon-135','half_life':135,'conc':28,'conc_err':2.3}]

    #template = Template(tStr)
    print template.render(nuclides=n_list, nid="12345")
    

def testXml2Html():
    
    r = XML2HTMLRenderer('/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates','ArrHtml.html')
    
    r.render('/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/ext/sampml-full-239646.xml')

def parserTest():
    
    # need to setup the ENV containing the the path to the conf file:
    os.environ[Conf._ENVNAME] = "/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/rnpicker.config"
    
    r = RequestParser()
    
    str = "spectrum=ALL, analysis=CURR/QC"
    
    print "split str = %s\n"%(str.split(','))
    
    d = r.parse(str)
    
    print "dict %s\n"%(d)
    

if __name__ == '__main__':
    
    testXml2Html()
   
    
    
    
    
    
    
   
  
   
