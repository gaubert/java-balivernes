
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
    
    def __init__(self,type,value,begin,end,line_num,parsed_line):
        
        self._type         = type
        self._value        = value
        self._begin        = begin
        self._end          = end
        self._parsed_line  = parsed_line
        self._line_num     = line_num
    
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
        return "Token[type=%s,value={%s},line_num=%s,(begin index,end index)=(%s,%s)"%(self._type,self._value,self._line_num,self._begin,self._end)  

class ENDMARKERToken(Token):
    """ A very special Token: ENDMARKER to signal the end of program """
    
    def __init__(self,a_line_num):
        
        super(ENDMARKERToken,self).__init__(ENDMARKER,None,-1,-1,a_line_num,"")

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
        return "ENDMARKER Token line_num = %d"%(self._line_num)  


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
ID_RE       = re.compile(r'[\*A-Za-z_+\(\)\<\>=][\<\>\(\)\w_\.@\*+-=]*')

# DATETIME Token
DATETIME    = 'DATETIME'
DATETIME_RE = re.compile(r'((19|20|21)\d\d)[-/.]?(0[1-9]|1[012]|[1-9])[-/.]?(0[1-9]|[12][0-9]|3[01]|[1-9])([tT ]?([0-1][0-9]|2[0-3]|[1-9])([:]?([0-5][0-9]|[1-9]))?([:]([0-5][0-9]|[1-9]))?([.]([0-9])+)?)?')

# NEWLINE Token
NEWLINE    = 'NEWLINE'
NEWLINE_RE = re.compile(r'\n+|(\r\n)+')

# MSGFORMAT Token
MSGFORMAT    = 'MSGFORMAT'
MSGFORMAT_RE = re.compile(r'[A-Za-z]{3}(\d+\.\d+)')

# Language keywords

# BEGIN 
BEGIN        = 'BEGIN'
BEGIN_RE     = re.compile('BEGIN',re.IGNORECASE)

STOP         = 'STOP'
STOP_RE      = re.compile('STOP',re.IGNORECASE)

TO           = 'TO'
TO_RE        = re.compile('TO',re.IGNORECASE)

MSGTYPE      = 'MSG_TYPE'
MSGTYPE_RE   = re.compile('MSG_TYPE',re.IGNORECASE)

MSGID        = 'MSG_ID'
MSGID_RE     = re.compile('MSG_ID',re.IGNORECASE)

EMAIL        = 'EMAIL'
EMAIL_RE     = re.compile('E-MAIL',re.IGNORECASE)

TIME         = 'TIME'
TIME_RE      = re.compile('TIME',re.IGNORECASE)

STALIST     = 'STALIST'
STALIST_RE  = re.compile('STA_LIST',re.IGNORECASE)

KEYWORDS_TOKENS = [BEGIN,STOP,TO,MSGTYPE,MSGID,EMAIL,TIME,STALIST]

TOKENS = {
           ID       : ID_RE,
           DATETIME : DATETIME_RE,
           NUMBER   : NUMBER_RE,
           MSGFORMAT: MSGFORMAT_RE,
           BEGIN    : BEGIN_RE,
           STOP     : STOP_RE,
           TO       : TO_RE,
           MSGTYPE  : MSGTYPE_RE,
           MSGID    : MSGID_RE,
           EMAIL    : EMAIL_RE,
           TIME     : TIME_RE,
           STALIST  : STALIST_RE,
           NEWLINE  : NEWLINE_RE,
         }

# key ordered to optimize pattern matching
# it also defines the pattern matching rule precedence
TOKENS_ORDERED = [DATETIME]  + KEYWORDS_TOKENS + [MSGFORMAT,ID,NUMBER,NEWLINE]

# Litterals to ignore
IGNORED_LITERALS = " \f\t\x0c"

# ENDMARKER Token to signal end of program
ENDMARKER = "ENDMARKER"


class IMSTokenizer(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.ims_tokenizer")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        # list of tokens
        self._tokens  = []
        
        self._index   = 0
        
        self._current = None
        
        self._io_prog = None
        
    def set_io_prog(self,a_io_prog):
        
        self._io_prog = a_io_prog
        
    def io_prog(self):
        return self._io_prog
        
    def tokenize(self):
        """ parse the expression.
        
            Args:
               a_expression: the expression to parser
               
            Returns:
               return dict containing the different parts of the request (spectrum, ....)
        
            Raises:
               exception CTBTOError if the syntax of the aString string is incorrect
        """
        
        line_num = 0
        
        for a_line in self._io_prog:
            print("line to read=[%s].len(line)=%d\n"%(a_line,len(a_line)))
            
            line_num    += 1
        
            pos, max = 0, len(a_line)
        
            while pos < max:
            
                b_found = False
                # This code provides some short-circuit code for whitespace, tabs, and other ignored characters
                if a_line[pos] in IGNORED_LITERALS:
                    pos += 1
                    continue
            
                print("Try to match from [%s]\n"%(a_line[pos:]))
                        
                for key in TOKENS_ORDERED:
                    regexp = TOKENS[key]
                    match  = regexp.match(a_line,pos)
                    if match:
                       
                        val        = match.group()
                        start, end = pos,(pos+len(val)-1)
                        tok        = Token(key,val,start,end,line_num,a_line)
                    
                        #update pos
                        pos = end +1
                    
                        #print("Token = %s\n"%(tok))
                        b_found = True
                    
                        #return token using yield and generator
                        yield tok
                        
                        #found on so quit for loop
                        break
            
            
                if not b_found:
                    LexerError("Illegal Character. Char to match %s"%(a_line[pos]),a_line,pos)
                    pos = max
            
        
        # All lines have been read return ENDMARKER Token
        yield ENDMARKERToken(line_num)
              
# unit tests part
import unittest
class TestTokenizer(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testTokenizerIterator(self):     
        
        # get simple string
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("\r\n 34543 342\n2009.05.04     Toto")
        
        tokenizer.set_io_prog(io_prog)
        
        #gen_tok = tokenizer.tokenize()
        
        for tok in tokenizer.tokenize():
            print("Tok = %s \n"%(tok))
            
            if tok.type == ENDMARKER:
                print("End of program\n")
                return 
        
        
        