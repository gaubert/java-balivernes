import os
import time
import itertools
import gc


class curry:
    """ Class used to implement the currification (functional programming technic) :
        Create a function from another one by instanciating some of its parameters.
        For example double = (operator.mul,2), res = double(4) = 8
    """
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

def round_as_string(aFloat,aNbDigits):
    """ Round a float number up to aNbDigits after the .
        printf is used to do that.
    
        Args:
           aFloat:    the float to round
           aNbDigits: the nb of digits to round after 
           
        Returns:
           a string representation of the rounded number
    
        Raises:
           exception
    """
    assert aNbDigits > 0
    
    # create string in two steps. There is surely a better way to do it in one step
    formatting_str = '%sf'%(aNbDigits)
    formatting_str = '%.' + '%sf'%(aNbDigits)
    
    return formatting_str%(float(aFloat))

def round(aFloat,aNbDigits):
    """ Round a float number up to aNbDigits after the .
        printf is used to do that.
    
        Args:
           aFloat:    the float to round
           aNbDigits: the nb of digits to round after 
           
        Returns:
           a rounded nb a a float
    
        Raises:
           exception
    """
    return float(round_as_string(aFloat, aNbDigits))

def checksum(aString):
    """checksum the passed string. This is a 32 bits checksum
    
        Args:
           params: aString. String from which the checksum is computed 
           
        Returns:
           return the checksum of the passed string
    
        Raises:
           exception
    """
        
    chksum = 0L
    toggle = 0

    i = 0
    while i < len(aString):
        ch = aString[i]
        if ord(ch) > 0:
            if toggle: chksum = chksum << 1
            chksum = chksum + ord(ch)
            chksum = chksum & 0X7fffffff
            toggle = not toggle
        else:
            chksum = chksum + 1
        i = i + 1

    return chksum

#####################################
#
#  check if a file exist and otherwise raise an exception
#
################################### 
def file_exits(aFilePath):
    
    # asserting input parameters
    if aFilePath == None:
        raise Exception(-1,"passed argument aFilePath is null")
    else:
        # check if file exits
        if not os.path.exists(aFilePath):
            raise Exception(-1,"the file %s does not exits"%(aFilePath))
        
def makedirs(aPath):
    """ my own version of makedir """
    
    if os.path.isdir(aPath):
        # it already exists so return
        return
    elif os.path.isfile(aPath):
        raise OSError("a file with the same name as the desired dir, '%s', already exists."%(aPath))

    os.makedirs(aPath)

def ftimer(func, args, kwargs, result = [], number=1, timer=time.time):
    """ time a func or object method """
    it = itertools.repeat(None, number)
    gc_saved = gc.isenabled()
    
    try:
       gc.disable()
       t0 = timer()
       for i in it:
         r = func(*args, **kwargs)
         if r is not None:
            result.append(r)
       t1 = timer()
    finally:
       if gc_saved:
          gc.enable()
        
    t = t1-t0 
    return t1 - t0
      


#####################################
#
#  print crudely a dict
#
################################### 
def printDict(di, format="%-25s %s"):
    """ pretty print a dictionary """
    for (key, val) in di.items():
        print format % (str(key)+':', val)
        

#####################################
#
#  dump data structure in a stream
#
################################### 
def dump(aData,aIostream=None):
    pp = pprint.PrettyPrinter(indent=4,stream=aIostream)
    pp.pprint(self._dataBag)
    

def printInFile(aStr,aPath):
    #check if it is a path or a file
     
    if str(aPath.__class__) == "<type 'str'>":
      f = open(aPath,"w")
    else:
      f = aPath
    
    f.write(aStr)
    f.close()
    
   
    
#####################################
#
#  pretty Format an Xml Tree
#
###################################  
def prettyFormatElem(elem,level=0):
    """ indent an xml tree """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            prettyFormatElem(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



            
if __name__ == "__main__":

    print "Hello"