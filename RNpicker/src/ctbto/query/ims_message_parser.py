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
        
        self._line_num = a_line_num
        self._pos      = a_pos
        
        if self._line_num == None and self._pos == None:
            extra = "" 
        else:
            extra = "(line=%s,pos=%s)"%(self._line_num,self._pos)
        
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
        return self._read_header_message()
    
    def _read_header_message(self):
        """ Read the 4 first lines that are considered as the "header of the message".
            This will help finding the message type
        
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
        # format: begin message_format
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
        
        # line 2: get the message type
        # format: msg_type request
        token = self._tokenizer.next()
        
        if token.type != Token.MSGTYPE:
            raise ParsingError("Expected a MSGTYPE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        
        if token.type != Token.ID:
            raise ParsingError("Expected a ID type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        result[Token.MSGTYPE] = token.value
        
        token = self._tokenizer.next()
        
        # look for a new line
        if token.type != Token.NEWLINE:
            raise ParsingError("Expected a NEWLINE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        
        # line 3: get the message id
        # format: msg_id id_string [source]
        if token.type != Token.MSGID:
            raise ParsingError("Expected a MSGID type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        
        # next token is an ID 
        # TODO: the id_string should be up to 20 characters and should not contains blanks or \
        if token.type != Token.ID and token.type != Token.NUMBER:
            raise ParsingError("Expected a ID type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        result[Token.MSGID] = token.value
        
        token = self._tokenizer.next()
        
        # it can be a source or a NEWLINE
        
        # this is a source and source format 3-letter country code followed by _ndc (ex: any_ndc)
        if token.type == Token.ID:
            result['SOURCE'] = token.value
        elif token.type != Token.NEWLINE:
            raise ParsingError("Expected an ID type as the source or a NEWLINE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        # look for a new line
        if token.type != Token.NEWLINE:
            raise ParsingError("Expected a NEWLINE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        # line 4: e-mail foo.bar@domain_name
        token = self._tokenizer.next()
        # look for an EMAIL keyword
        if token.type != Token.EMAIL:
            raise ParsingError("Expected a NEWLINE type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        token = self._tokenizer.next()
        # look for the EMAILADDR
        if token.type != Token.EMAILADDR:
            raise ParsingError("Expected an EMAILADDR type but instead got %s with type %s"%(token.value,token.type),token.line_num,token.begin)
        
        result[Token.EMAIL] = token.value
        
        
        return result
           
        

       