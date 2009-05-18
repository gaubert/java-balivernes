'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org

'''
import logging
import StringIO

from ims_tokenizer import IMSTokenizer, Token, LexerError, NonExistingTokenError, TokensNotFoundError

class ParsingError(Exception):
    """Base class for All exceptions"""

    def __init__(self,a_msg,a_line_num=None,a_pos=None):
        
        self._line_num = a_line
        self._pos      = a_pos
        
        if self._line == None and self._pos == None:
            extra = "" 
        else:
            extra = "(line=%s,pos=%s)"%(self._line,self._pos)
        
        super(ParsingError,self).__init__("%s %s."%(a_msg,extra))
    
    #def __str__(self):
    #    return "ParsingError (line:%s,col:%s) => %s"%()
        

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
         
        self._tokenizer.set_io_prog(io_prog)
        
        return self._parse()
    
    def _parse(self):
        """ private parsing method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """
        return self._read_message()
    
    def _read_message(self):
        """ read a message.
        
            Args: None
               
            Returns:
               return a dictionary of values 
        
            Raises:
               exception 
        """ 
        result = {}
        
        # might need to advance until a BEGIN token
        # for the moment check if the first token is a begin
        token = self._tokenizer.next()
        curr_line_num = 0
        
        # look for line 1 BEGIN message_format
        if token.type != Token.BEGIN:
            raise ParsingError("Expected the message to start with a BEGIN type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        
        # look for a message_format
        if token.type != Token.MSGFORMAT:
            raise ParsingError("Expected a MSGFORMAT type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        result[Token.MSGFORMAT] = token.value
        
        
        token = self._tokenizer.next()
        
        # look for a new line
        if token.type != Token.NEWLINE:
            raise ParsingError("Expected a NEWLINE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        # get the message type
        token = self._tokenizer.next()
        
        if token.type != Token.MSGTYPE:
            raise ParsingError("Expected a MSGTYPE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        
        if token.type != Token.ID:
            raise ParsingError("Expected a ID type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        result[Token.MSGTYPE] = token.value
        
        return result
           
        

       