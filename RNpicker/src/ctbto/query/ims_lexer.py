'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org
'''

import re
from ply.lex import TOKEN #pylint: disable-msg=F0401
import ply.lex  as lex #pylint: disable-msg=F0401

# Base Class for the Parser and Lexer errors
class SyntaxError(Exception):
    """Syntax Error exceptions. Base Class for the parser and lexer errors"""

    def __init__(self, a_message, a_token): #pylint: disable-msg=E1003
        super(Exception,self).__init__(a_message)
        self._message         = a_message
        self._token           = a_token
        self._expected_terminals = []
        
    @property
    def message(self):
        return self._message
    
    @property
    def lineno(self):
        return self._token.lexer.lineno if self._token != None else -1
    
    @property
    def pos(self):
        start_of_line         = self._token.lexer.line_offsets[self._token.lexer.lineno-1]
        return (self._token.lexer.lexpos - start_of_line)-1 if self._token != None else -1
    
    @property
    def unknown_token(self):
       raise Exception("needs to be defined in children") 
    
    @property
    def token(self):
        return self._token
    
    def get_expected_terminals(self):
        return self._expected_terminals
    
    def set_expected_terminals(self, a_values):
        self._expected_terminals = a_values
        
    
    property(get_expected_terminals,set_expected_terminals)
    
    @property
    def original_string(self):
        lineno                = self._token.lexer.lineno
        start_of_line         = self._token.lexer.line_offsets[lineno-1]
        end_of_line           = self._token.lexer.line_offsets[lineno]
        return self._token.lexer.lexdata[start_of_line:end_of_line]

    def __repr__(self):
        raise Exception("Method should be implemented in children")

    def __str__(self):
        return self.__repr__()
    
class LexerError(SyntaxError):
    
    def __init__(self,a_message,a_token):
        super(LexerError,self).__init__(a_message,a_token)
    
    def __repr__(self):
        """ redefined to manage a LexerError """
        
        if self._token != None:
            lineno, lexpos, lexer = self._token.lexer.lineno , self._token.lexer.lexpos , self._token.lexer
            start_of_line                = lexer.line_offsets[lineno-1]
            end_of_line                  = lexer.line_offsets[lineno]
            original_request             = lexer.lexdata[start_of_line:end_of_line]
            offset                       = (lexpos - start_of_line)
            
            #request with error 
            instrumented_request  = original_request[:offset] + "(ERR)=>" + original_request[offset:]
             
            return "Error(%s) in (line,pos) = (%s,%s):\n%s."%(self.message,lineno,offset,instrumented_request)
        else:
            return "%s"%(self.message)
    
    @property
    def unknown_token(self):
        """ return the first character of the matched token"""
        return self._token.value[0] if self._token != None else 'No characters'

class IMSLexer(object):
    """
       Lexer Object encapsulating the ply lexer and providing extra services such as get current token.
       This object is iterable.
    """
    
    _newline_pattern = re.compile(r"\n")
    
    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self._lexer             = lex.lex(debug=debug, optimize=optimize, lextab=lextab, reflags=reflags)
        self._token_stream      = None
        self._current_token     = None
        # original string to parse
        self._original_string   = None
    
    def input(self, s, add_endmarker=True):
        """ 
           pass a new string to tokenize to the tokenizer 
        """
        self._lexer.paren_count = 0
        self._original_string   = s
        self._lexer.line_offsets = self._get_line_offsets(s)
        # lower case for the expression. It is case-insensitive
        #self._lexer.input(s.lower())
        self._lexer.input(s)
        
        self._token_stream      = self._create_token_stream(self._lexer,add_endmarker)
        
    def _get_line_offsets(self,text):
        offsets = [0]
        for m in IMSLexer._newline_pattern.finditer(text):
            offsets.append(m.end())
        # This is only really needed if the input does not end with a newline
        offsets.append(len(text))
        return offsets
        
    def __iter__(self):
        """ support iterable interface """
        return self

    def next(self):
        """ return the next token from the token stream """
        self._current_token = self._token_stream.next()
        return self._current_token

    def token(self):
        """ return the next token from the token stream. same as next but complies with the ply interface """
        self._current_token = self._token_stream.next()
        return self._current_token

    def current_token(self):
        """ return the current token """
        return self._current_token

    def _create_token_stream(self,lexer,add_endmarker=True):
        """ create the stream of token and insert an ENDMARKER when necessary """
        
        token = None
        ttokens = iter(self._lexer.token, None)
        for token in ttokens:
            yield token

        if add_endmarker:
            lineno = 1
            lexpos = -1
            if token is not None:
                lineno = token.lineno
                lexpos = token.lexpos
            yield self._new_token("ENDMARKER",lineno,lexpos)

    def _new_token(self,type, lineno,lexpos=-1):
        """ private method for creating tokens like ENDMARKER """
        tok = lex.LexToken()
        tok.type   = type
        tok.value  = None
        tok.lineno = lineno
        tok.lexpos = lexpos
        return tok
    
    def get_ply_lexer(self):
        """ return the ply lexer """
        return self._lexer


############################ Private Stuff gor the module ####################################################
############################ This part contains the PLY cooking stuff ########################################

### Lexer: change to your own risks

# functor tools to assemble tokens
def group(*choices)   : return '(' + '|'.join(choices) + ')'
def any(*choices)     : return group(*choices) + '*'
def maybe(*choices)   : return group(*choices) + '?'


# lexer part
# Reserved general keywords for the language (not technology secific)
# Structural keywords
structural_language_keywords = ( 
                     'PART',
                     'TO',
                     'BEGIN',
                     'STOP',
                     'OF',
                )

language_keywords = (
                     'MSG_TYPE',
                     'MSG_ID',
                     'REF_ID',
                     'PROD_ID',
                     'TIME',
                     'TIME_STAMP',
                     'LAT',
                     'LON',
                     'STA_LIST',
                     'CHAN_LIST',
                     'HELP',
                    )

# all reserved words
reserved = structural_language_keywords + language_keywords 

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r


# lexing rules
tokens = reserved + ( 
    # Literals (identifier, number, DATETIME, string)
    'MSGFORMAT', 'ID','WCID','DATA','DATETIME', 'NUMBER',
    
    # Transports
    'EMAIL','FTP',
    
    # Separator
    'COMMA','SLASH','COLON', 'SQUAREBRA', 'SQUAREKET',
    
    # NEWLINE (might not be needed)
    'NEWLINE',
    
    # Stop support extra lines added by mailer MessageSize, Sender and =
    'MINUS'
) 

#Only to support extra lines added by mailer
t_COMMA            = r','
t_SLASH            = r'/'
t_COLON            = r':'
t_MINUS            = r'-'

@TOKEN(r'\[')
def t_SQUAREBRA(t):
    t.lexer.paren_count += 1
    return t

@TOKEN(r'\]')
def t_SQUAREKET(t):
    t.lexer.paren_count -= 1
    return t

# date time pattern
# With the separator between years,months and days being either - or / or nothing or .
# Format supported YYYY[-/.]MM[-/.]DD[tT ]HH:MM:SS.s
DateTime ="((19|20|21)\d\d)[-/.]?(0[1-9]|1[012]|[1-9])[-/.]?(0[1-9]|[12][0-9]|3[01]|[1-9])([tT ]?([0-1][0-9]|2[0-3]|[1-9])([:]?([0-5][0-9]|[1-9]))?([:]([0-5][0-9]|[1-9]))?([.]([0-9])+)?)?"

@TOKEN(DateTime)
def t_DATE_TIME(t):
    t.type = "DATETIME"
    # TODO add the date time object need a converter
    #t.value =
    #print "matched DATETIME VALUE %s\n"%(t.value) 
    return t

# Take the numbering system from tokenize module
Octnumber = r'0[0-7]*[lL]?'
Decnumber = r'[1-9]\d*[lL]?'
Intnumber = group(Decnumber)
Exponent = r'[eE][-+]?\d+'
Pointfloat = group(r'\d+\.\d*', r'\.\d+') + maybe(Exponent)
Expfloat = r'\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group(r'\d+[jJ]', Floatnumber + r'[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

# The NUMBER tokens return a 2-ple of (value, original string)

# The original string can be used to get the span of the original
# token and to provide better round-tripping.

# imaginary numbers in Python are represented with floats,
#   (1j).imag is represented the same as (1.0j).imag -- with a float
@TOKEN(Imagnumber)
def t_IMAG_NUMBER(t):
    t.type = "NUMBER"
    t.value = (float(t.value[:-1])* 1j, t.value)
    return t

# Then check for floats (must have a ".")
@TOKEN(Floatnumber)
def t_FLOAT_NUMBER(t):
    t.type = "NUMBER"
    t.value = (float(t.value), t.value)
    return t

@TOKEN(Octnumber)
def t_OCT_NUMBER(t):
    t.type = "NUMBER"
    value = t.value
    if value[-1] in "lL":
        value = value[:-1]
        f = long
    else:
        f = int
    t.value = (f(value, 8), t.value)
    return t

@TOKEN(Decnumber)
def t_DEC_NUMBER(t):
    r"[1-9][0-9]*[lL]?"
    t.type = "NUMBER"
    value = t.value
    if value[-1] in "lL":
        value = value[:-1]
        f = long
    else:
        f = int
    t.value = (f(value, 10), t.value)
    return t

# Ignored whitespace and tab characters 
t_ignore = " \f\t\x0c"

def t_MSGFORMAT(t):
    r'[A-Za-z]{3}(\d+\.\d+)'
    t.type = "MSGFORMAT"
    return t

def t_EMAIL(t):
    r'e-mail'
    t.type ="EMAIL"
    return t

# Identifiers and reserved words
def t_ID(t):
    r'[\*A-Za-z_+\(\)\<\>=][\<\>\(\)\w_\.@\*+-=]*'   
    #r'[\*A-Za-z_+][\w_\.@\*+-]*'
    # if string is longer than 55 bytes, it is most probably a data
    if len(t.value) > 55:
        t.type = 'DATA'
    # check if it contains a * if yes then type=WCID (wildcard ID) 
    elif t.value.lower().find('*') >= 0:
        t.type = "WCID"
        # if this is a minus
    elif t.value.lower().find('-') >= 0:
        t.type = 'DATA'
    else:
        t.type = reserved_map.get(t.value.lower(),"ID")
    return t


def t_NEWLINE(t):
    r'\n+|(\r\n)+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t
    
def t_error(t): 
    raise LexerError("Illegal character '%s'"%(t.value[0]),t)  
    
