'''
Created on Dec 11, 2009

@author: guillaume.aubert@ctbto.org
'''
import error_commons

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=====
# To manage arguments

class ParsingError(error_commons.CLIError):
    """Error when the command line is parsed"""

    def __init__(self, a_error_msg):
        super(ParsingError, self).__init__()
        self._error_message = a_error_msg
        
    def get_message_error(self):
        """ return error message """
        return self._error_message

def reassociate_arguments(a_args):
    """
        reassociate arguments passed in the program arguments when they are spearated by a space.
        a, b , c will become 'a, b ,c'
    """
    the_list = len(a_args)
    
    if the_list <= 1:
        return a_args
    else:
        res = []
        _reassoc_arguments(a_args[0], a_args[1:], res)
        return res

def _reassoc_arguments(head, tail, res, memo=''): 
    """
            private function used to recurse in reassociate_arguments
    """
    # stop condition, no more fuel
    if len(tail) == 0:
        # if command separate
        if head.startswith('-'):
            res.extend([memo, head])
            return
        else:
            res.append(memo + head)
            return
    
    if head.endswith(',') or head.startswith(','):
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo + head)
    elif head.startswith('-'):
        # we do have a command so separate it from the rest
        if len(memo) > 0:
            res.append(memo)
            
        res.append(head)
        
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, '')
    else:  
        # it is not a command 
        _reassoc_arguments(tail[0], tail[1:] if len(tail) > 1 else [], res, memo + head) 
            
    
