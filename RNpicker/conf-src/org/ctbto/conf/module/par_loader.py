'''
Created on Feb 1, 2010

@author: guillaume.aubert@ctbto.org
'''

import re
import os

class Error(Exception):
    """Base class for ConfigParser exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class ParsingError(Error):
    """Raised when a configuration file does not follow legal syntax."""
    def __init__(self, filename):
        Error.__init__(self, 'File contains parsing errors: %s' % filename)
        self.filename = filename
        self.errors = []

    def append(self, lineno, line):
        """ add error message """
        self.errors.append((lineno, line))
        self.message += '\n\t[line %2d]: %s' % (lineno, line)
        
    def get_error(self):
        """ return the error """
        return self
    
OPTCRE = re.compile(
        r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
        r'\s*(?P<vi>[:=])\s*'                 # any number of space/tab,
                                              # followed by separator
                                              # (either : or =), followed
                                              # by any # space/tab
        r'(?P<value>.*)$'                     # everything up to eol
        )

#higher than in a normal conf system because par is messy
MAX_INCLUDE_DEPTH = 20

def _read_include(a_original_file, lineno, include_file, depth):
    """ read an included par file """
    # Error if depth is MAX_INCLUDE_DEPTH 
    if depth >= MAX_INCLUDE_DEPTH:
        raise ParsingError("Cannot do more than %d nested includes. It is probably a mistake as you might have created a loop of includes." % (MAX_INCLUDE_DEPTH))
    
    if not os.path.exists(include_file):
        raise ParsingError("Include PAR file %s declared lineno %d of %s doesn't exist." % (include_file, lineno, a_original_file))

    # add include file and populate the section hash
    return read(include_file, depth + 1)

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
        var = toparse[index:closing_brack_index + 1]
        
        m = self._SUBSGROUPRE.match(var)
    
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



def read(a_path, a_depth = 0):
    ''' read a par file '''
    
    lineno = 0
    err    = None
    the_section = {} 
    
    the_fp = open(a_path) 
    
    while True:
        line = the_fp.readline()
        if not line:
            break
        lineno = lineno + 1
        
        # to be changed include in this form %include
        if line.startswith('%include'):
            #self._read_include(lineno, line, fpname, depth)
            continue
        # comment or blank line?
        if line.strip() == '' or line[0] in '#;':
            continue
        else:
            the_match = OPTCRE.match(line)
            if the_match:
                optname, vi, optval = the_match.group('option', 'vi', 'value')
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
                
                optname = optname.rstrip().lower()
                
                # if optname = par then it is an include
                if optname == 'par':
                    to_merge_dict = _read_include(a_path, lineno, optval, a_depth)
                    the_section.update(to_merge_dict)
                    
                the_section[optname] = optval
            else:
                # a non-fatal parsing error occurred.  set up the
                # exception but keep going. the exception will be
                # raised at the end of the file and will contain a
                # list of all bogus lines
                if not err:
                    err = ParsingError(a_path)
                err.append(lineno, repr(line))
    
    the_fp.close()   
                     
    return the_section
    