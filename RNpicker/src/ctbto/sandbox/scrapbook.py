#from StringIO import StringIO
#import operator
#import string
import subprocess
import base64
import os
import zlib
import ctbto.common.utils
#import ctbto.common.time_utils as time_utils
import re

import tokenize
import StringIO




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
    
    print "S=%s\n"%(s)

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

def testXml2Html():
    
    r = XML2HTMLRenderer('/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates','ArrHtml.html')
    
    result = r.render('/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/ext/sampml-full-239646.xml')
    
    utils.printInFile(result,"/tmp/Transformed.html")

def parserTest():
    
    # need to setup the ENV containing the the path to the conf file:
    #IGNORE:W0212
    os.environ[Conf._ENVNAME] = "/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/rnpicker.config"
    
    r = RequestParser()
    
    lStr = "spectrum=ALL, analysis=CURR/QC"
    
    print "split str = %s\n"%(lStr.split(','))
    
    d = r.parse(lStr,'PAR')
    
    print "dict %s\n"%(d)
    
def _get_closing_bracket_index(index,s):
    
    tolook = s[index+2:]
   
    openingBrack = 1
    closing_brack_index = index+2
    
    i = 0
    for c in tolook:
        if c == ')':
            if openingBrack == 1:
                return closing_brack_index
            else:
                openingBrack -= 1
     
        elif c == '(':
            if tolook[i-1] == '%':
                openingBrack +=1
        
        # inc index
        closing_brack_index +=1
        i += 1
    
    return closing_brack_index
    
def replace_vars(a_str):
    
    data = {'Hello':{'one':'1','two':'2'},'Bye':{'trois':'one','quatre':'4'}}
     
    toparse = a_str
    
    index = toparse.find("%(")
    
    reg = re.compile(r"%\((?P<group>\w*)\[(?P<option>(.*))\]\)")
    # if found opening %( look for end bracket)
    if index >= 0:
        # look for closing brackets while counting openings one
        closing_brack_index = _get_closing_bracket_index(index,a_str)
        
        print "closing bracket %d"%(closing_brack_index)
        var = toparse[index:closing_brack_index+1]
        m = reg.match(var)
        
        if m == None:
            print "Error. Cannot match a %(group[option]) in %s but found an opening bracket %(. Probably malformated expression"%(var)
        else:
            
            print "found %s[%s]\n"%(m.group('group'),m.group('option'))
            
            g = replace_vars(m.group('group'))
            o = replace_vars(m.group('option'))
            
            try:
                dummy = data[g][o]
            except KeyError, ke: #IGNORE:W0612
                print "Error, property %s[%s] doesn't exist in this configuration file \n"%(g,o)
                return None
            
            
            toparse = toparse.replace(var,dummy)
            
            return replace_vars(toparse)
             
    else:   
        return toparse 
   
   
  
token_pat = re.compile("\s*(?:(\d+)|(.))")

class literal_token(object):
    def __init__(self, value):
        self.value = int(value)
    def nud(self):
        return self.value

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

class operator_add_token(object):
    lbp = 10
    def led(self, left):
        right = expression(10)
        return left + right

class end_token(object):
    lbp = 0


def my_tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield literal_token(number)
        elif operator == "+":
            yield operator_add_token()
        else:
            raise SyntaxError("unknown operator")
    yield end_token()

def parse(program):
    global token, next
    next = my_tokenize(program).next
    token = next()
    return expression()

def python_tokenizer(program):
    
    result = []
    g = tokenize.generate_tokens(StringIO.StringIO(program).readline)   # tokenize the string
    for toknum, tokval, tok3, tok4,_  in g:
      result.append((toknum, tokval, tok3, tok4))

    return result
   
def test_tokenizer():
    
    #res = parse("1 + 2")
    
    #res = python_tokenizer("retrieve spectrum.a where mdc > 2")
    res = python_tokenizer("retrieve spectrum[CURR,BK,SPHD] where techno = radionuclide and id = 1234567 and mdc= 124.56 in  file=\"/tmp/produced.data\", filetype=\"SAMPML\"")
    
    print "res = %s\n"%(res)
    
    import token
    
    print "Token Name: %s\n"%(token.tok_name[1]) 
    
    

if __name__ == '__main__':
    
    test_tokenizer()

   
    
    
    
    
    
    
   
  
   
