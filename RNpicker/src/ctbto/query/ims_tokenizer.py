
"""
Tokenizer parsing the grammar
"""
import logging
import StringIO
import re

class LexerError(Exception):
    """Base class for All exceptions"""

    def __init__(self,a_msg,a_line=None,a_col=None):
        
        self._line = a_line
        self._col  = a_col
        
        if self._line == None and self._col == None:
            extra = "" 
        else:
            extra = "(line=%s,col=%s)"%(self._line,self._col)
        
        super(LexerError,self).__init__("%s %s."%(a_msg,extra))
    

class Token(object):
    
    def __init__(self,type,num,value,begin,end,parsed_line):
        
        self._type  = type
        self._num   = num
        self._value = value
        self._begin = begin
        self._end   = end
        self._parsed_line  = parsed_line
    
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
    def parsed_line(self):
        """ Return the token line """
        return self._parsed_line
    
    def __repr__(self):
        return "[type,num]=[%s,%s],value=[%s], parsed line=%s,[begin index,end index]=[%s,%s]"%(self._type,self._num,self._value,self._parsed_line,self._begin,self._end)
         

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

WS          = 'WS'
WS_RE       = re.compile(r'[ \f\t]*')

TOKENS = {
           ID       : ID_RE,
           DATETIME : DATETIME_RE,
           NUMBER   : NUMBER_RE,
           WS       : WS_RE,
         }

# key ordered to optimize pattern matching
TOKENS_ORDERED = [WS,ID,NUMBER,DATETIME]


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
            print("Try to match from [%s]\n"%(a_line[pos:]))
                        
            for key in TOKENS_ORDERED:
                regexp = TOKENS[key]
                match  = regexp.match(a_line,pos)
                if match:
                    # scan for tokens
                    start, end = match.span(1)
                    spos, epos, pos = (a_line_num, start), (a_line_num, end), end
                    token = a_line[start:end]
                    print("(token,type) = (%s,%s)\n"%(token,key))
                    b_found = True
                    break
            
            
            if not b_found:
                print("didn't find anything else")
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
         
        tokens.tokenize(" 34543 342")
        