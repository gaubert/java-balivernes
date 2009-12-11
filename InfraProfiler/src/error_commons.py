'''
Created on Dec 11, 2009

@author: guillaume.aubert@ctbto.org
'''
import cStringIO
import traceback
import sys

class CLIError(Exception):
    """ Base class exception """
    pass

def get_exception_traceback():
    """
            return the exception traceback (stack info and so on) in a string
        
            Args:
               None
               
            Returns:
               return a string that contains the exception traceback
        
            Raises:
               
    """
    the_file = cStringIO.StringIO()
    exception_type, exception_value, exception_traceback = sys.exc_info() #IGNORE:W0702
    traceback.print_exception(exception_type, exception_value, exception_traceback, file = the_file)
    return the_file.getvalue()

class ConfAccessError(CLIError):
    """The only exception where a logger as not yet been set as it depends on the conf"""

    def __init__(self, a_error_msg):
        super(ConfAccessError, self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        """ return error message """
        return self._error_message