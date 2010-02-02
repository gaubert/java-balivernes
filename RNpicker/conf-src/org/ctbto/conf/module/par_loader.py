'''
Created on Feb 1, 2010

@author: guillaume.aubert@ctbto.org
'''

import re

from ctbto.common.exceptions import CTBTOError

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

def read(a_path):
    ''' read a par file '''
    
    lineno = 0
    err = None 
    
    #the section to return
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
    