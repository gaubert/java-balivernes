""" 
    Copyright 2008 CTBTO Organisation
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    module: configuration env
"""
#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import re

import resource

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

class NoSectionError(Error):
    """Raised when no section matches a requested option."""

    def __init__(self, section):
        Error.__init__(self, 'No section: %r' % (section,))
        self.section = section

class SubstitutionError(Error):
    """Base class for substitution-related exceptions."""

    def __init__(self, lineno,location, msg):
        Error.__init__(self,'SubstitutionError on line %d: %s. %s'%(lineno,location,msg) if lineno !=-1 else 'SubstitutionError in %s. %s'%(lineno,location,msg))
        
class IncludeError(Error):
    """ Raised when an include command is incorrect """
    
    def __init__(self, msg, origin):
        Error.__init__(self,msg)
        self.origin = origin
        self.errors = []


class ParsingError(Error):
    """Raised when a configuration file does not follow legal syntax."""

    def __init__(self, filename):
        Error.__init__(self, 'File contains parsing errors: %s' % filename)
        self.filename = filename
        self.errors = []

    def append(self, lineno, line):
        self.errors.append((lineno, line))
        self.message += '\n\t[line %2d]: %s' % (lineno, line)
        
class MissingSectionHeaderError(ParsingError):
    """Raised when a key-value pair is found before any section header."""

    def __init__(self, filename, lineno, line):
        ParsingError.__init__(
            self,
            'File contains no section headers.\nfile: %s, line: %d\n%r' %
            (filename, lineno, line))
        self.filename = filename
        self.lineno = lineno
        self.line = line

class Conf(object):
    """ 
       Configuration Object with a several features:
       - get configuration info in different types
       - support for import
       - support for variables in configuration file
       - support for default values in all accessors
       - integrated with the resources object offering to get the configuration from an env var, a commandline option or the conf
       - to be done : support for blocs, list comprehension and dict comprehension, json 
       - to be done : define resources in the conf using the [Resource] group with A= { ENV:TESTVAR, CLI:--testvar, VAL:1.234 }
    
    """
    # command line and env resource stuff
    CLINAME ="--conf_file"
    ENVNAME ="CONF_FILE" 
    
    #class member
    _instance = None
    
    _CLIGROUP          = "CLI"
    _ENVGROUP          = "ENV"
    _MAX_INCLUDE_DEPTH = 10
    
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = Conf()
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
            
    
    def __init__(self,use_resource=True):
        
        # create resource for the conf file
        self._confResource = resource.Resource(Conf.CLINAME,Conf.ENVNAME)
        
        # list of sections
        self._sections = {}
        
        self._configuration_file_path = None
        
        # create config object 
        if use_resource:       
            self._load_config()
        

   
    def _load_config(self,aFile=None):
        try:  
            # get it from a Resource if not files are passed
            if aFile is None:
                aFile = self._confResource.getValue() 
             
            if aFile is None:
                raise CTBTOError("Conf. Error, need a configuration file path\n")
            
            fp = open(aFile,'r') 
                
            self._read(fp,aFile)
            
            # memorize conf file path
            self._configuration_file_path = aFile
            
        except Exception, e:
            print "Can't read the config file %s"%(aFile)
            print "Current executing from dir = %s\n"%(os.getcwd())
            raise e
            
            #raise ContextError(-1,"Can't read the config file %s"%(aFile))
    
    def get_conf_file_path(self):
        return self._configuration_file_path if self._configuration_file_path != None else "unknown"
       
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
            return str(default)
    
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
            #check if it is a ENV section
            dummy = None
            if section == Conf._ENVGROUP:
                r     = resource.Resource(CliArgument=None,EnvVariable=opt)
                dummy = r.getValue()
            elif section == Conf._CLIGROUP:
                r     = resource.Resource(CliArgument=opt,EnvVariable=None)
                dummy = r.getValue()
            #return default if dummy is None otherwise return dummy
            return ( (self._get_defaults(default,fail_if_missing)) if dummy == None else dummy )
        elif opt in self._sections[section]:
            return self._replace_vars(self._sections[section][opt],"%s[%s]"%(section, option),-1)
        else:
            return self._get_defaults(default,fail_if_missing)

    def items(self, section):
        """ return all items from a section. Items is a list of tuples (option,value)
            
            Args:
               section. The section where to find the option
               
            Returns: a list of tuples (option,value)
        
            Raises:
               exception NoSectionError if the section cannot be found
        """
        try:
            d2 = self._sections[section]
            # make a copy
            d = d2.copy()
            # remove __name__ from d
            if "__name__" in d:
                del d["__name__"]
                
            return d.items()
        
        except KeyError:
            raise NoSectionError(section)

    def has_option(self, section, option):
        """Check for the existence of a given option in a given section."""
        
        if section not in self._sections:
            return False
        else:
            option = self.optionxform(option)
            return (option in self._sections[section])
    
    def _get_closing_bracket_index(self,index,s,location,lineno):
        """ private method used by _replace_vars to count the closing brackets.
            
            Args:
               index. The index from where to look for a closing bracket
               s. The string to parse
               group. group and options that are substituted. Mainly used to create a nice exception message
               option. option that is substituted. Mainly used to create a nice exception message
               
            Returns: the index of the found closing bracket
        
            Raises:
               exception NoSectionError if the section cannot be found
        """
        
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
    
        raise SubstitutionError(lineno,location,"Missing a closing bracket in %s"%(tolook))

    # very permissive regex
    _SUBSGROUPRE = re.compile(r"%\((?P<group>\w*)\[(?P<option>(.*))\]\)")
    
    def _replace_vars(self,a_str,location,lineno=-1):
        """ private replacing all variables. A variable will be in the from of %(group[option]).
            Multiple variables are supported, ex /foo/%(group1[opt1])/%(group2[opt2])/bar
            Nested variables are also supported, ex /foo/%(group[%(group1[opt1]].
            Note that the group part cannot be substituted, only the option can. This is because of the Regular Expression _SUBSGROUPRE that accepts only words as values.
            
            Args:
               index. The index from where to look for a closing bracket
               s. The string to parse
               
            Returns: the final string with the replacements
        
            Raises:
               exception NoSectionError if the section cannot be found
        """
 
        toparse = a_str
    
        index = toparse.find("%(")
    
        # if found opening %( look for end bracket)
        if index >= 0:
            # look for closing brackets while counting openings one
            closing_brack_index = self._get_closing_bracket_index(index,a_str,location,lineno)
        
            #print "closing bracket %d"%(closing_brack_index)
            var = toparse[index:closing_brack_index+1]
            
            m = self._SUBSGROUPRE.match(var)
        
            if m == None:
                raise SubstitutionError(lineno,location,"Cannot match a group[option] in %s but found an opening bracket (. Malformated expression "%(var))
            else:
            
                # recursive calls
                g = self._replace_vars(m.group('group'),location,-1)
                o = self._replace_vars(m.group('option'),location,-1)
            
                try:
                    # if it is in ENVGROUP then check ENV variables with a Resource object
                    # if it is in CLIGROUP then check CLI argument with a Resource object
                    # otherwise check in standard groups
                    if g == Conf._ENVGROUP:
                        r = resource.Resource(CliArgument=None,EnvVariable=o)
                        dummy = r.getValue()
                    elif g == Conf._CLIGROUP:
                        r = resource.Resource(CliArgument=o,EnvVariable=None)
                        dummy = r.getValue()
                    else:
                        dummy = self._sections[g][self.optionxform(o)]
                except KeyError, ke: #IGNORE:W0612
                    raise SubstitutionError(lineno,location,"Property %s[%s] doesn't exist in this configuration file \n"%(g,o))
            
            toparse = toparse.replace(var,dummy)
            
            return self._replace_vars(toparse,location,-1)    
        else:   
            return toparse 


    def _get(self, section, conv, option, default,fail_if_missing):
        return conv(self.get(section, option,default,fail_if_missing))

    def getint(self, section, option, default=None,fail_if_missing=False):
        return self._get(section, int, option, default,fail_if_missing)

    def getfloat(self, section, option, default=None,fail_if_missing=False):
        return self._get(section, float, option, default,fail_if_missing)

    _boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                       '0': False, 'no': False, 'false': False, 'off': False}

    def getboolean(self, section, option, default=None,fail_if_missing=False):
         
        v = self.get(section, option, default,fail_if_missing)
        if v.lower() not in self._boolean_states:
            raise ValueError, 'Not a boolean: %s' % v
        return self._boolean_states[v.lower()]
    
    def getlist(self,section, option, default=None,fail_if_missing=False):
        """ get a list of string """
        v = self.get(section, option, default,fail_if_missing)
        l = v.split(',')
        return l
        
        
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

    def _read_include(self,lineno,line,origin,depth):
        
        # Error if depth is MAX_INCLUDE_DEPTH 
        if depth >= Conf._MAX_INCLUDE_DEPTH:
            raise IncludeError("Error. Cannot do more than %d nested includes. It is probably a mistake as you might have created a loop of includes"%(Conf._MAX_INCLUDE_DEPTH))
        
        # remove %include from the path and we should have a path
        i = line.find('%include')
        
        path = line[i+8:].strip() 
        
        # replace variables if there are any
        path = self._replace_vars(path,line,lineno)
        
        # check if file exits
        if not os.path.exists(path):
            raise IncludeError("the config file to include %s does not exits"%(path),origin)
        else:
            fp = open(path,'r')
            # add include file and populate the section hash
            self._read(fp,path,depth+1)

    def _read(self, fp, fpname,depth=0):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        Depth for avoiding looping in the includes
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
            # include in this form %include
            if line.startswith('%include'):
                self._read_include(lineno,line,fpname,depth)
                continue
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
            raise e #IGNORE:E0702

# unit tests part
import unittest
import sys
import org.ctbto.conf

def tests():
    suite = unittest.TestLoader().loadTestsFromModule(org.ctbto.conf)
    unittest.TextTestRunner(verbosity=2).run(suite)

class TestConf(unittest.TestCase):
    
    def _get_tests_dir_path(self):
        """ get the org.ctbto.conf.tests path depending on where it is defined """
        
        fmod_path = org.ctbto.conf.__path__
        
        test_dir = "%s/tests"%fmod_path[0]
        
        return test_dir
    
    def setUp(self):
         
        # necessary for the include with the VAR ENV substitution
        os.environ["DIRCONFENV"] = self._get_tests_dir_path()
         
        self.conf = Conf(use_resource=False)
    
        fp = open('%s/%s'%(self._get_tests_dir_path(),"test.config"))
    
        self.conf._read(fp,"the file") #IGNORE:W0212
        
    def testAPrintModulePath(self):
        
        print("org.ctbto.conf module is loaded from %s\n"%(self._get_tests_dir_path()))
    
    def testGetObjects(self):
        """testGetObjects: test getter from all types """
        # get simple string
        astring = self.conf.get("GroupTest1","astring")
        
        self.assertEqual(astring,"oracle.jdbc.driver.OracleDriver")
        
        # get an int
        aint = self.conf.getint("GroupTest1","aint")
        
        self.assertEqual(aint,10)
        
        # get floatcompile the statements
        afloat = self.conf.getfloat("GroupTest1","afloat")
        
        self.assertEqual(afloat,5.24)
        
        # get different booleans form
        abool1 = self.conf.getboolean("GroupTest1","abool1")
        
        self.assertEqual(abool1,True)
        
        abool2 = self.conf.getboolean("GroupTest1","abool2")
        
        self.assertEqual(abool2,False)
        
        abool3 = self.conf.getboolean("GroupTest1","abool3")
        
        self.assertEqual(abool3,True)
        
        abool4 = self.conf.getboolean("GroupTest1","abool4")
        
        self.assertEqual(abool4,False)
        
    def testGetDefaults(self):
        """testGetDefaults: test defaults values """
        
         # get all defaults
        astring = self.conf.get("GroupTest","astring","astring")
        
        self.assertEqual(astring,"astring")
        
        # get an default for int
        aint = self.conf.getint("GroupTest","aint",2)
        
        self.assertEqual(aint,2)
        
         # get float
        afloat = self.conf.getfloat("GroupTest","afloat",10.541)
        
        self.assertEqual(afloat,10.541)
        
        abool1 = self.conf.getboolean("GroupTest","abool1",True)
        
        self.assertEqual(abool1,True)
        
        abool2 = self.conf.getboolean("GroupTest","abool2",False)
        
        self.assertEqual(abool2,False)
        
        # existing group no option
        abool5 = self.conf.getboolean("GroupTest1","abool32",False)
        
        self.assertEqual(abool5,False)
        
    def testVarSubstitutions(self):
        """testVarSubstitutions: test variables substitutions"""
        
        # simple substitution
        apath = self.conf.get("GroupTestVars","path")
        
        self.assertEqual(apath,"/foo/bar//tmp/foo/bar/bar/foo")
        
        # multiple substitution
        apath = self.conf.get("GroupTestVars","path1")
        
        self.assertEqual(apath,"/foo//tmp/foo/bar//foo/bar//tmp/foo/bar/bar/foo/bar")
        
        # nested substitution
        nested = self.conf.get("GroupTestVars","nested")
        
        self.assertEqual(nested,"this is done")  
        
    def testInclude(self):
        """testInclude: test includes """
        val = self.conf.get("IncludedGroup","hello")
        
        self.assertEqual(val,'foo')
        
    def _create_fake_conf_file_in_tmp(self):
        
        f = open('/tmp/fake_conf.config','w')
        
        f.write('\n[MainDatabaseAccess]\n')
        f.write('driverClassName=oracle.jdbc.driver.OracleDriver')
        f.flush()
        f.close()
    
    def testUseConfENVNAMEResource(self):
        """testUseConfENVNAMEResource: Use default resource ENVNAME to locate conf file"""
        self._create_fake_conf_file_in_tmp()
        
        # need to setup the ENV containing the the path to the conf file:
        os.environ[Conf.ENVNAME] = "/tmp/fake_conf.config"
   
        self.conf = Conf.get_instance()
        
        s = self.conf.get("MainDatabaseAccess","driverClassName")
        
        self.assertEqual(s,'oracle.jdbc.driver.OracleDriver')
    
    def testReadFromCLI(self):
        """testReadFromCLI: do substitutions from command line resources"""
        #set environment
        os.environ["TESTENV"] = "/tmp/foo/foo.bar"
        
        val = self.conf.get("GroupTest1","fromenv")
   
        self.assertEqual(val,'/mydir//tmp/foo/foo.bar')
        
        #set cli arg
        sys.argv.append("--LongName")
        sys.argv.append("My Cli Value")
        
        val = self.conf.get("GroupTest1","fromcli1")
   
        self.assertEqual(val,'My Cli Value is embedded')
        
        #check with a more natural cli value
        val = self.conf.get("GroupTest1","fromcli2")
   
        self.assertEqual(val,'My Cli Value is embedded 2')
    
    def testReadFromENV(self):
        """testReadFromENV: do substitutions from ENV resources"""
        #set environment
        os.environ["TESTENV"] = "/tmp/foo/foo.bar"
        
        val = self.conf.get("ENV","TESTENV")
        
        self.assertEqual(val,"/tmp/foo/foo.bar")
        
        #set cli arg
        sys.argv.append("--LongName")
        sys.argv.append("My Cli Value")
        
        val = self.conf.get("CLI","LongName")
        
        self.assertEqual(val,"My Cli Value")
        
        # get a float from env
        os.environ["TESTENV"] = "1.05"
        
        val = self.conf.getfloat("ENV","TESTENV")
        
        self.assertEqual(val+1,2.05) 

        
if __name__ == '__main__':
    tests()