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
        
def makedirs(aPath):
    """ my own version of makedir """
    
    if os.path.isdir(aPath):
        # it already exists so return
        return
    elif os.path.isfile(aPath):
        raise OSError("a file with the same name as the desired dir, '%s', already exists."%(aPath))

    os.makedirs(aPath)

        



class Conf:
    """ 
       Configuration Singleton Class used to access configuration information
       Wrapper over ConfigParser.
       It implements a default behavior.  
    
    """
    
    #class member
    _instance = None
    
    def get_instance(cls):
        if Conf._instance == None:
            Conf._instance = Conf()
        return Conf._instance
    
    def __init__(self):
        # create config object
        self._load_config()

   
    def _load_config(self,aFile="/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/rnpicker.config"):
        try:
            # [MAJ] can take a file list with default
            self._conf  = ConfigParser.ConfigParser()
            self._conf.read(aFile)
        except:
            print "Can't read the config file %s"%(aFile)
            print "Current executing from dir = %s\n"%(os.getcwd())
            
            #raise ContextError(-1,"Can't read the config file %s"%(aFile))

    get_instance    = classmethod(get_instance)
    
    def sections(self):
        """Return a list of section names, excluding [DEFAULT]"""
        
        return self._conf.sections()

    def add_section(self, section):
        """Create a new section in the configuration.

        Raise DuplicateSectionError if a section by the specified name
        already exists.
        """
        self._conf.add_section(section)
       

    def has_section(self, section):
        """Indicate whether the named section is present in the configuration.

        The DEFAULT section is not acknowledged.
        """
        return self._conf.has_section(section)

    def options(self, section):
        """Return a list of option names for the given section name."""
        return self._conf.options(section)

    def read(self, filenames):
        """Read and parse a filename or a list of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify a list of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the list will be read.  A single
        filename may also be given.

        Return list of successfully read files.
        """
        return self._conf.read(filenames)

    def readfp(self, fp, filename=None):
        """Like read() but the argument must be a file-like object.

        The `fp' argument must have a `readline' method.  Optional
        second argument is the `filename', which if not given, is
        taken from fp.name.  If fp has no `name' attribute, `<???>' is
        used.

        """
        self._conf.readfp(fp,filename)

    def get(self, section, option, default=None, raw=False, vars=None):
        """ get with a default """
        try:
          return self._conf.get(section, option, raw, vars)
        except ConfigParser.NoOptionError, nOE:
            # no elements found return the default
            return default
        

    def items(self, section):
        return self._conf.items(section)


    def getint(self, section, option,default=None):
        
        try:
          return self._conf.getint(section, option)
        except ConfigParser.NoOptionError, nOE :
            # no elements found return the default if not None otherwise propagate exception
            if default is None:
                raise nOE
            else:
                return default

    def getfloat(self, section, option,default=None):
       
        try:
          return self._conf.getfloat(section, option)
        except ConfigParser.NoOptionError, nOE :
            # no elements found return the default if not None otherwise propagate exception
            if default is None:
                raise nOE
            else:
                return default

    def getboolean(self, section, option,default=None):
       
        try:
          return self._conf.getboolean(section, option)
        except ConfigParser.NoOptionError, nOE :
            # no elements found return the default if not None otherwise propagate exception
            if default is None:
                raise nOE
            else:
                return default

    def optionxform(self, optionstr):
        return self._conf.optionxform(optionstr)

    def has_option(self, section, option):
        """Check for the existence of a given option in a given section."""
        return self._conf.has_option(section,option)

    def set(self, section, option, value):
        """Set an option."""
        self._conf.set(section,option,value)

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        self._conf.write(fp)

    def remove_option(self, section, option):
        """Remove an option."""
        self._conf.remove(section,option)

    def remove_section(self, section):
        """Remove a file section."""
        self._conf.remove_section(section)


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