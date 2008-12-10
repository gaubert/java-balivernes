

import os
import re

# exception classes
class Error(Exception):
    """Base class for ConfigParser exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__
    
class NoOptionError(Error):
    """A requested option was not found."""

    def __init__(self, option, section):
        Error.__init__(self, "No option %r in section: %r" %
                       (option, section))
        self.option = option
        self.section = section

class PowerConf(object):
    """ 
       Configuration Object with a several features:
       - get configuration info in different types
       - support for import
       - support for variables in configuration file
       - support for default values in all accessors
       - integrated with the resources object offering to get the configuration from an env var, a commandline option or the conf
       - support for blocs, list comprehension and dict comprehension, json 
    
    """
    # command line and env resource stuff
    CLINAME ="--power_conf_file"
    ENVNAME ="POWER_CONF_FILE" 
    
    #class member
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = PowerConf()
        return cls._instance
    
    @classmethod
    def can_be_instanciated(cls):
        """Class method used by the Resource to check that the Conf can be instantiated.
           This two objects have a special contract as they are strongly coupled:
           A Resource can use the Conf to check for a Resource and the Conf uses a Resource to read Conf filepath
        
            Returns:
               return True if the Conf file has got a file
        
            Raises:
               exception
        """
        #No conf info passed to the resource so the Resource will not look into the conf (to avoid recursive search)
        r = resource.Resource(cls.CLINAME,cls.ENVNAME)
        
        filepath = r.getValue(aRaiseException=False)
        
        if (filepath is not None) and os.path.exists(filepath):
            return True
        
        return False
            
    
    def __init__(self):
        
        # create resource for the conf file
        #self._confResource = resource.Resource(Conf.CLINAME,Conf.ENVNAME)
        
        # list of sections
        self._sections = {}
       
    def sections(self):
        """Return a list of section names, excluding [DEFAULT]"""
        # self._sections will never have [DEFAULT] in it
        return self._sections.keys()
    
    def _get_defaults(self,default,fail_if_missing):
        """ To manage defaults.
            Args:
               default. The default value to return if fail_if_missing is False
               fail_if_missing. Throw an exception when the option is not found and fail_if_missing is true
               
            Returns: default if fail_if_missing is False
        
            Raises:
               exception NoOptionError if fail_if_missing is True
        """
        if fail_if_missing:
            raise NoOptionError(option,section)  
        else:
            return default
    
    def get(self, section, option, default=None,fail_if_missing=False):
        """ get one option from a section.
            return the default if it is not found and if fail_if_missing is False, otherwise return NoOptionError
          
            Args:
               section. The section where to find the option
               option.  The option to get
               default. The default value to return if fail_if_missing is False
               fail_if_missing. Throw an exception when the option is not found and fail_if_missing is true
               
            Returns: the option as a string
        
            Raises:
               exception NoOptionError if fail_if_missing is True
        """
        # all options are kept in lowercase
        opt = self.optionxform(option)
        
        if section not in self._sections:
            self._get_defaults(default,fail_if_missing)
        elif opt in self._sections[section]:
            return self._sections[section][opt]
        else:
            self._get_defaults(default,fail_if_missing)

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
        return optionstr.lower()
    
     #
    # Regular expressions for parsing section headers and options.
    #
    SECTCRE = re.compile(
        r'\['                                 # [
        r'(?P<header>[^]]+)'                  # very permissive!
        r'\]'                                 # ]
        )
    OPTCRE = re.compile(
        r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
        r'\s*(?P<vi>[:=])\s*'                 # any number of space/tab,
                                              # followed by separator
                                              # (either : or =), followed
                                              # by any # space/tab
        r'(?P<value>.*)$'                     # everything up to eol
        )

    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        """
        cursect = None                            # None, or a dictionary
        optname = None
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname] = "%s\n%s" % (cursect[optname], value)
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    else:
                        cursect = {'__name__': sectname}
                        self._sections[sectname] = cursect
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise MissingSectionHeaderError(fpname, lineno, line)
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if vi in ('=', ':') and ';' in optval:
                            # ';' is a comment delimiter only if it follows
                            # a spacing character
                            pos = optval.find(';')
                            if pos != -1 and optval[pos-1].isspace():
                                optval = optval[:pos]
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = self.optionxform(optname.rstrip())
                        cursect[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

if __name__ == '__main__':
    
    c = PowerConf()
    
    fp = open("/home/aubert/projects/java-balivernes/RNpicker/etc/conf/rnpicker.config")
    
    c._read(fp,"the file")