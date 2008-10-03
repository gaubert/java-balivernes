import os

import ConfigParser


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

###################################  
#
#  Class Conf
#
################################### 
class Conf:
    """ Configuration Static Class. used to access configuration information """
    _conf = None

    def get_conf(cls):
        if Conf._conf == None:
            Conf.load_config()
        return Conf._conf

    def load_config(cls,aFile="../etc/conf/rnpicker.config"):
        try:
            # [MAJ] can take a file list with default
            Conf._conf  = ConfigParser.ConfigParser()
            Conf._conf.read(aFile)
        except:
            print "Can't read the config file %s"%(aFile)
            print "Current executing from dir = %s\n"%(os.getcwd())
            
            #raise ContextError(-1,"Can't read the config file %s"%(aFile))

    load_config = classmethod(load_config)
    get_conf    = classmethod(get_conf)


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