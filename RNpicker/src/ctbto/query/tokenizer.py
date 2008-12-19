
"""
Tokenizer parsing the grammar
"""
import logging
import tokenize
import token
import StringIO

class Token(object):
    
    def __init__(self,type,num,value,begin,end,line):
        
        self._type  = type
        self._num   = num
        self._value = value
        self._begin = begin
        self._end   = end
        self._line  = line
    
    @property
    def type(self):
        """ Return the token type """
        return self._type

    @property
    def num(self):
        """ Return the token type num """
        return self._num

    @property
    def value(self):
        """ Return the token value """
        return self._value
    
    @property
    def begin(self):
        """ Return the token begin """
        return self._begin
    
    @property
    def end(self):
        """ Return the token end """
        return self._end
    
    @property
    def line(self):
        """ Return the token line """
        return self._line
    
    def __repr__(self):
        return "[type,num]=[%s,%s],value=[%s],line=%s,[begin index,end index]=[%s,%s]"%(self._type,self._num,self._value,self._line,self._begin,self._end)
         

class Tokenizer(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.Tokenizer")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        # list of tokens
        self._tokens  = []
        
        self._index   = 0
        
        self._current = None
       
    def tokenize(self,a_program):
        """ parse the expression.
        
            Args:
               a_expression: the expression to parser
               
            Returns:
               return dict containing the different parts of the request (spectrum, ....)
        
            Raises:
               exception CTBTOError if the syntax of the aString string is incorrect
        """
        g = tokenize.generate_tokens(StringIO.StringIO(a_program).readline)   # tokenize the string
        
        for toknum, tokval, tokbeg, tokend,tokline  in g:
            self._tokens.append(Token(token.tok_name[toknum],toknum, tokval, tokbeg, tokend,tokline))
        
    def _generator(self):
        for tok in self._tokens:
            self._current = tok
            yield tok
            
    def __iter__(self):
        for tok in self._tokens:
            self._current = tok
            yield tok
        
    def next(self):
        self._current = self._tokens[self._index]
        self._index += 1
        return self._current
    
    def has_next(self):
        return self._index < len(self._tokens)
    
    def current_token(self):
        return self._current
    
    def advance(self):
        return self._tokens[self._index+1]
     
    
            
            
# unit tests part
import unittest
class TestTokenizer(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testTokenizer(self):
        
        # get simple string
        tokens = Tokenizer()
        
        #tokens.tokenize("retrieve spectrum[CURR,BK] where technology = radionuclide and id=123456 in file=\"/tmp/ctbto.data\", filetype=SAMPML")
        
        tokens.tokenize("retrieve spectrum where i>3")
        
        t = tokens.next()
        
        print "t = %s\n"%(t)
        
        for tok in tokens:
            print "Token = %s \n"%(tok)  
            
          
            
            