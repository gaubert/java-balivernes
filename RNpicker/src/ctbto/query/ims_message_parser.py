'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org

'''
import logging

from ims_tokenizer import IMSTokenizer, Token, LexerError, NonExistingTokenError, TokensNotFoundError


class IMSParser(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.IMSParser")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        
        self._tokenizer = IMSTokenizer()
        
        # io stream
        self._io_prog   = None
    
    def parse(self,message):
        """ parsed the passed message.
        
            Args:
               message: the message to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        # For the moment the message is always a string
        io_prog = StringIO.StringIO(message)
         
        tokenizer.set_io_prog(io_prog)
        
        return self._parse()
    
    def _parse(self):
        pass

       