
"""
Tokenizer parsing the grammar
"""
import logging
import StringIO
import re

class LexerError(Exception):
    """Base class for All exceptions"""

    def __init__(self,a_msg,a_line=None,a_pos=None):
        
        self._line = a_line
        self._pos  = a_pos
        
        if self._line == None and self._pos == None:
            extra = "" 
        else:
            extra = "(line=%s,pos=%s)"%(self._line,self._pos)
        
        super(LexerError,self).__init__("%s %s."%(a_msg,extra))
    

class Token(object):
    
    def __init__(self,type,value,begin,end,parsed_line):
        
        self._type  = type
        self._value = value
        self._begin = begin
        self._end   = end
        self._parsed_line  = parsed_line
    
    @property
    def type(self):
        """ Return the token type """
        return self._type

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
    def parsed_line(self):
        """ Return the token line """
        return self._parsed_line
    
    def __repr__(self):
        return "Token[type=%s,value={%s},parsed line=%s,(begin index,end index)=(%s,%s)"%(self._type,self._value,self._parsed_line,self._begin,self._end)
     
    def __str__(self):
        return self.__repr__()    

# functor tools to assemble tokens
def group(*choices)   : return '(' + '|'.join(choices) + ')'
def any(*choices)     : return group(*choices) + '*'
def maybe(*choices)   : return group(*choices) + '?'

# NUMBER Token
NUMBER = 'NUMBER'

#regular expressions for number
Hexnumber = r'0[xX][\da-fA-F]*[lL]?'
Octnumber = r'0[0-7]*[lL]?'
Decnumber = r'[1-9]\d*[lL]?'
Intnumber = group(Hexnumber, Octnumber, Decnumber)
Exponent = r'[eE][-+]?\d+'
Pointfloat = group(r'\d+\.\d*', r'\.\d+') + maybe(Exponent)
Expfloat = r'\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group(r'\d+[jJ]', Floatnumber + r'[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

NUMBER_RE = re.compile(Number)

# ID Token
ID          = 'ID'
Id          = r'[\*A-Za-z_+\(\)\<\>=][\<\>\(\)\w_\.@\*+-=]*'
ID_RE       = re.compile(Id)

# DATETIME Token
DATETIME    = 'DATETIME'
Datetime    = r'((19|20|21)\d\d)[-/.]?(0[1-9]|1[012]|[1-9])[-/.]?(0[1-9]|[12][0-9]|3[01]|[1-9])([tT ]?([0-1][0-9]|2[0-3]|[1-9])([:]?([0-5][0-9]|[1-9]))?([:]([0-5][0-9]|[1-9]))?([.]([0-9])+)?)?'
DATETIME_RE = re.compile(Datetime)

# NEWLINE Token
NEWLINE    = 'NEWLINE'
NEWLINE_RE = re.compile(r'\n+|(\r\n)+')

TOKENS = {
           ID       : ID_RE,
           DATETIME : DATETIME_RE,
           NUMBER   : NUMBER_RE,
           NEWLINE  : NEWLINE_RE,
         }

# key ordered to optimize pattern matching
TOKENS_ORDERED = [ID,NUMBER,DATETIME,NEWLINE]

IGNORED_LITERALS = " \f\t\x0c"


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
        

    def _tokenize_line(self,a_line,a_line_num):
        """ find tokens in a line """
        
        pos, max = 0, len(a_line)
        
        while pos < max:
            
            b_found = False
            # This code provides some short-circuit code for whitespace, tabs, and other ignored characters
            if a_line[pos] in IGNORED_LITERALS:
                pos += 1
                continue
            
            # check if it is a NEWLINE 
            
            
            print("Try to match from [%s]\n"%(a_line[pos:]))
                        
            for key in TOKENS_ORDERED:
                regexp = TOKENS[key]
                match  = regexp.match(a_line,pos)
                if match:
                    # scan for tokens
                    print("match.group() = [%s], match.lastindex = %s\n"%(match.group(),match.lastindex))
                    
                    val        = match.group()
                    start, end = pos,(pos+len(val)-1)
                    tok        = Token(key,val,start,end,a_line)
                    
                    #update pos
                    pos = end +1
                    
                    #print("(token,type) = (%s,%s)\n"%(val,key))
                    print("Token = %s\n"%(tok))
                    b_found = True
                    break
            
            
            if not b_found:
                LexerError("Illegal Character. Char to match %s"%(a_line[pos]),a_line,pos)
                pos = max
            
                
        
        
        
    def tokenize(self,a_program):
        """ parse the expression.
        
            Args:
               a_expression: the expression to parser
               
            Returns:
               return dict containing the different parts of the request (spectrum, ....)
        
            Raises:
               exception CTBTOError if the syntax of the aString string is incorrect
        """
        io_prog = StringIO.StringIO(a_program)
          
        line_num = 1
        
        for line in io_prog:
            print("line to read=[%s].len(line)=%d\n"%(line,len(line)))
            line_tokens = self._tokenize_line(line,line_num)
            line_num    += 1
            
    def __iter__(self):
        """ iterator implemented with a generator.
        """
        for tok in self._tokens:
            self._current = tok
            yield tok
        
    def next(self):
        """ get next token.
          
            Returns:
               return next token
        """
        
        self._current = self._tokens[self._index]
        self._index += 1
        return self._current
    
    def has_next(self):
        """ check it there are more tokens to consume.
        
            Returns:
               return True if more tokens to consume False otherwise
        """
        return self._index < len(self._tokens)
    
    def current_token(self):
        """ return the latest consumed token.
        
            Returns:
               return the latest consumerd token
        """
        return self._current
    
    def consume_token(self,what):
        if self._current.value != what :
            raise LexerError("Expected '%s' but instead found '%s'"%(what,self._current.value))
        else:
            return self.next()
    
    def advance(self,inc=1):
        """ return the next + inc token but do not consume it.
            Useful to check future tokens.
        
            Args:
               a_expression: increment + 1 is the default (just look one step forward)
               
            Returns:
               return lookhead token
        """
        return self._tokens[self._index-1+inc]
     
    
            
            
# unit tests part
import unittest
class TestTokenizer(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testTokenizerIterator(self):     
        
        # get simple string
        tokens = Tokenizer()
         
        tokens.tokenize("\r\n 34543 342\n     Toto")
        