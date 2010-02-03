"""
    :Summary: conf_helper, configuration management 
    :Creation date: 2008-09-03
    :Version: 1.0
    :Authors: guillaume.aubert@ctbto.org

"""

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
"""

import os
import re

import resource
from org.ctbto.conf.exceptions import Error, NoOptionError, NoSectionError, \
                                      SubstitutionError, IncludeError, ParsingError, \
                                      MissingSectionHeaderError
                                      
from utils.struct_parser import Compiler, CompilerError

import utils.module_loader as module_loader
 


class Conf(object):
    """ Configuration Object with a several features:
    
         * get configuration info in different types
         * support for import
         * support for variables in configuration file
         * support for default values in all accessors
         * integrated with the resources object offering to get the configuration from an env var, a commandline option or the conf
         * to be done : support for blocs, list comprehension and dict comprehension, json 
         * to be done : define resources in the conf using the [Resource] group with A= { ENV:TESTVAR, CLI:--testvar, VAL:1.234 }
    
    """
    # command line and env resource stuff
    CLINAME = "--conf_file"
    ENVNAME = "CONF_FILE" 
    
    #class member
    _instance = None
    
    _CLIGROUP = "CLI"
    _ENVGROUP = "ENV"
    _MAX_INCLUDE_DEPTH = 10
    
    @classmethod
    def get_instance(cls):
        """ singleton method """
        if cls._instance == None:
            cls._instance = Conf()
        return cls._instance
    
    @classmethod
    def can_be_instanciated(cls):
        """Class method used by the Resource to check that the Conf can be instantiated. 
        
        These two objects have a special contract as they are strongly coupled. 
        A Resource can use the Conf to check for a Resource and the Conf uses a Resource to read Conf filepath.
        
        :returns: True if the Conf file has got a file.
           
        :except Error: Base Conf Error
        
        """
        #No conf info passed to the resource so the Resource will not look into the conf (to avoid recursive search)
        the_res = resource.Resource(cls.CLINAME, cls.ENVNAME)
        
        filepath = the_res.getValue(aRaiseException=False)
        
        if (filepath is not None) and os.path.exists(filepath):
            return True
        
        return False
            
    
    def __init__(self, use_resource=True):
        #TODO docstring ==> use resource ????
        
        # create resource for the conf file
        self._conf_resource = resource.Resource(Conf.CLINAME, Conf.ENVNAME)
        
        # list of sections
        self._sections = {}
        
        self._configuration_file_path = None
        
        # create config object 
        if use_resource:       
            self._load_config()
        

   
    def _load_config(self, a_file = None):
        """ _load the configuration file """
        try:  
            # get it from a Resource if not files are passed
            if a_file is None:
                a_file = self._conf_resource.getValue() 
             
            if a_file is None:
                raise Error("Conf. Error, need a configuration file path")
            
            f_desc = open(a_file, 'r') 
                
            self._read(f_desc, a_file)
            
            # memorize conf file path
            self._configuration_file_path = a_file
            
        except Exception, exce:
            print "Can't read the config file %s" % (a_file)
            print "Current executing from dir = %s\n" % (os.getcwd())
            raise exce
            
    
    def get_conf_file_path(self):
        return self._configuration_file_path if self._configuration_file_path != None else "unknown"
       
    def sections(self):
        """Return a list of section names, excluding [DEFAULT]"""
        # self._sections will never have [DEFAULT] in it
        return self._sections.keys()
    
    def _get_defaults(self, section, option, default, fail_if_missing):
        """ To manage defaults.
            Args:
               default. The default value to return if fail_if_missing is False
               fail_if_missing. Throw an exception when the option is not found and fail_if_missing is true
               
            Returns: default if fail_if_missing is False
        
            Raises:
               exception NoOptionError if fail_if_missing is True
        """
        if fail_if_missing:
            raise Error(2, "No option %s in section %s" %(option, section))
        else:
            if default is not None:
                return str(default)
            else:
                return None
    
    def get(self, section, option, default=None, fail_if_missing=False):
        """ get one option from a section.
        
            return the default if it is not found and if fail_if_missing is False, otherwise return NoOptionError
          
            :param section: Section where to find the option
            :type  section: str
            :param option:  Option to get
            :param default: Default value to return if fail_if_missing is False
            :param fail_if_missing: Will throw an exception when the option is not found and fail_if_missing is true
               
            :returns: the option as a string
            
            :except NoOptionError: Raised only when fail_is_missing set to True
        
        """
        # all options are kept in lowercase
        opt = self.optionxform(option)
        
        if section not in self._sections:
            #check if it is a ENV section
            dummy = None
            if section == Conf._ENVGROUP:
                r = resource.Resource(CliArgument=None, EnvVariable=opt)
                dummy = r.getValue()
            elif section == Conf._CLIGROUP:
                r = resource.Resource(CliArgument=opt, EnvVariable=None)
                dummy = r.getValue()
            #return default if dummy is None otherwise return dummy
            return ((self._get_defaults(section, opt, default, fail_if_missing)) if dummy == None else dummy)
        elif opt in self._sections[section]:
            return self._replace_vars(self._sections[section][opt], "%s[%s]" % (section, option), - 1)
        else:
            return self._get_defaults(section, opt, default, fail_if_missing)
        
    
    def print_content(self, substitute_values = True):
        """ print all the options variables substituted.
        
            :param a_substitue_vals: bool for substituting values
            :returns: the string containing all sections and variables
        """
        
        result_str = ""
        
        for section_name in self._sections:
            result_str += "[%s]\n" % (section_name)
            section = self._sections[section_name]
            for option in section:
                if option != '__name__':
                    if substitute_values:
                        result_str += "%s = %s\n" % (option, self.get(section_name, option))
                    else:
                        result_str += "%s = %s\n" % (option, self._sections[section_name][option])
            
            result_str += "\n"
        
        return result_str
            

    def items(self, section):
        """ return all items from a section. Items is a list of tuples (option,value)
            
            Args:
               section. The section where to find the option
               
            Returns: a list of tuples (option,value)
        
            Raises:
               exception NoSectionError if the section cannot be found
        """
        try:
            all_sec = self._sections[section]
            # make a copy
            a_copy = all_sec.copy()
            # remove __name__ from d
            if "__name__" in a_copy:
                del a_copy["__name__"]
                
            return a_copy.items()
        
        except KeyError:
            raise NoSectionError(section)

    def has_option(self, section, option):
        """Check for the existence of a given option in a given section."""
        has_option = False
        if self.has_section(section):
            option = self.optionxform(option)
            has_option = (option in self._sections[section])
        return has_option
    
    def has_section(self, section):
        """Check for the existence of a given section in the configuration."""
        has_section = False
        if section in self._sections:
            has_section = True
        return has_section
        
    def _get_closing_bracket_index(self, index, s, location, lineno):
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
        
        tolook = s[index + 2:]
   
        opening_brack = 1
        closing_brack_index = index + 2
    
        i = 0
        for _ch in tolook:
            if _ch == ')':
                if opening_brack == 1:
                    return closing_brack_index
                else:
                    opening_brack -= 1
     
            elif _ch == '(':
                if tolook[i - 1] == '%':
                    opening_brack += 1
        
            # inc index
            closing_brack_index += 1
            i += 1
    
        raise SubstitutionError(lineno, location, "Missing a closing bracket in %s" % (tolook))

    # very permissive regex
    _SUBSGROUPRE = re.compile(r"%\((?P<group>\w*)\[(?P<option>(.*))\]\)")
    
    def _replace_vars(self, a_str, location, lineno= - 1):
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
            closing_brack_index = self._get_closing_bracket_index(index, a_str, location, lineno)
        
            #print "closing bracket %d"%(closing_brack_index)
            var   = toparse[index:closing_brack_index + 1]
            
            dummy = None
            
            m     = self._SUBSGROUPRE.match(var)
        
            if m == None:
                raise SubstitutionError(lineno, location, "Cannot match a group[option] in %s but found an opening bracket (. Malformated expression " % (var))
            else:
            
                # recursive calls
                g = self._replace_vars(m.group('group'), location, - 1)
                o = self._replace_vars(m.group('option'), location, - 1)
            
                try:
                    # if it is in ENVGROUP then check ENV variables with a Resource object
                    # if it is in CLIGROUP then check CLI argument with a Resource object
                    # otherwise check in standard groups
                    if g == Conf._ENVGROUP:
                        r = resource.Resource(CliArgument=None, EnvVariable=o)
                        dummy = r.getValue()
                    elif g == Conf._CLIGROUP:
                        r = resource.Resource(CliArgument=o, EnvVariable=None)
                        dummy = r.getValue()
                    else:
                        dummy = self._sections[g][self.optionxform(o)]
                except KeyError, _: #IGNORE:W0612
                    raise SubstitutionError(lineno, location, "Property %s[%s] doesn't exist in this configuration file \n" % (g, o))
            
            toparse = toparse.replace(var, dummy)
            
            return self._replace_vars(toparse, location, - 1)    
        else:   
            return toparse 


    def _get(self, section, conv, option, default, fail_if_missing):
        """ Internal getter """
        return conv(self.get(section, option, default, fail_if_missing))

    def getint(self, section, option, default=0, fail_if_missing=False):
        """Return the int value of the option.
        Default value is 0, None value can't be used as default value"""
        return self._get(section, int, option, default, fail_if_missing)

    def getfloat(self, section, option, default=0, fail_if_missing=False):
        """Return the float value of the option. 
        Default value is 0, None value can't be used as default value"""
        return self._get(section, float, option, default, fail_if_missing)

    _boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                       '0': False, 'no': False, 'false': False, 'off': False}

    def getboolean(self, section, option, default=False, fail_if_missing=False):
         
        v = self.get(section, option, default, fail_if_missing)
        if v.lower() not in self._boolean_states:
            raise ValueError, 'Not a boolean: %s' % v
        return self._boolean_states[v.lower()]
    
    def get_list(self, section, option, default=None, fail_if_missing=False):
        """ get a list of string """
        
        val = self.get(section, option, default, fail_if_missing)
        
        # parse it and return an error if invalid
        try:
            compiler = Compiler()
            return compiler.compile_list(val)
        except CompilerError, err: 
            raise Error(err.message)
    
    def getlist(self, section, option, default=None, fail_if_missing=False):
        """ Deprecated, use get_list instead"""
        return self.get_list(section, option, default, fail_if_missing)

    def getdict(self, section, option, default=None, fail_if_missing=False):
        """ Deprecated, use get_dict instead"""
        return self.get_dict(section, option, default, fail_if_missing)
        
    
    def get_dict(self, section, option, default=None, fail_if_missing=False):
        """ get a dict """
        
        val = self.get(section, option, default, fail_if_missing)
        
        # parse it and return an error if invalid
        try:
            compiler = Compiler()
            return compiler.compile_dict(val)
        except CompilerError, err: 
            raise Error(err.message)
        
        
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
    
    def _read_with_module(self, a_group_name, a_format, a_path, a_origin):
        """ read external include file that is defined in another format """
        
         # check if file exits
        if not os.path.exists(a_path):
            raise IncludeError("the config %s file to include %s does not exits" % (a_format, a_path), a_origin)
        
        mod_prefix = "org.ctbto.conf.module."
        
        # get the module dir from the current module path
        # then split the path from org to get only the dir where the src are defined
        current_mod_path = os.path.dirname(__file__)
        src_dir    = current_mod_path.split('org')[0]
        
        # need to get the module dir from the conf
        
        the_module = module_loader.load("%s%s_loader" %(mod_prefix,a_format), src_dir)
        
        cursect    = the_module.read(a_path)
        
        self._sections[a_group_name] = cursect
        
    def _read_include(self, lineno, line, origin, depth):
        
        # Error if depth is MAX_INCLUDE_DEPTH 
        if depth >= Conf._MAX_INCLUDE_DEPTH:
            raise IncludeError("Error. Cannot do more than %d nested includes. It is probably a mistake as you might have created a loop of includes" % (Conf._MAX_INCLUDE_DEPTH))
        
        # remove %include from the path and we should have a path
        i = line.find('%include')
        
        #check if there is a < for including config files from a different format
        #position after include
        i = i + 8
        
        # include file with a specific reading module
        if line[i] == '<':
            dummy = line[i+1:].strip()
            f_i = dummy.find('>')
            if f_i == -1:
                raise IncludeError("Error. > is missing in the include line no %s: %s. It should be %include<mode:group_name> path" % (line, lineno), origin )
            else:
                group_name = None
                format     = dummy[:f_i].strip()
                
                the_list = format.split(':')
                if len(the_list) != 2 :
                    raise IncludeError("Error. The mode and the group_name are not in the include line no %s: %s. It should be %include<mode:group_name> path" % (line, lineno), origin )
                else:
                    format, group_name = the_list
                    #strip the group name
                    group_name = group_name.strip()
                    
                path = dummy[f_i+1:].strip()
                
                # replace variables if there are any
                path = self._replace_vars(path, line, lineno)
                
                self._read_with_module(group_name, format, path, origin)
        else:
            # normal include   
            path = line[i:].strip() 
            
            # replace variables if there are any
            path = self._replace_vars(path, line, lineno)
            
            # check if file exits
            if not os.path.exists(path):
                raise IncludeError("the config file to include %s does not exits" % (path), origin)
            else:
                fp = open(path, 'r')
                # add include file and populate the section hash
                self._read(fp, path, depth + 1)

    def _read(self, fp, fpname, depth=0):
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
        err = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # include in this form %include
            if line.startswith('%include'):
                self._read_include(lineno, line, fpname, depth)
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
                            if pos != - 1 and optval[pos - 1].isspace():
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
                        if not err:
                            err = ParsingError(fpname)
                        err.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if err:
            raise err.get_error()
