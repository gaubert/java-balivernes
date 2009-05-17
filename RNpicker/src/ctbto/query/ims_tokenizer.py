'''
Created on May 16, 2009

@author: guillaume.aubert@ctbto.org
'''

import logging
import StringIO
import re

class LexerError(Exception):
    """LexerError Class"""

    def __init__(self,a_line_num,a_line,a_pos):
        
        self._line     = a_line
        self._pos      = a_pos
        self._line_num = a_line_num
        
        instrumented_request  = a_line[:a_pos] + "(ERR)=>" + a_line[a_pos:]
        
        msg = "Illegal Character %s in Line %d, position %d.[%s]"%(a_line[a_pos],a_line_num,a_pos,instrumented_request)
        
        super(LexerError,self).__init__(msg)
        
    @property    
    def line(self):
        return self._line
    
    @property
    def line_num(self):
        return self._line_num
    
    @property
    def pos(self):
        return self._pos
    
    def illegal_character(self):
        return self._line[self._pos]

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
#witout slash
#ID_RE       = re.compile(r'[\*A-Za-z_\+=\(\)\<\>]([\w]|[=\<\>\(\)\.@\*\+-])*')
ID_RE       = re.compile(r'[/\*A-Za-z_\+=\(\)\<\>]([\w]|[/=\<\>\(\)\.@\*\+-])*')

# DATETIME Token
DATETIME    = 'DATETIME'
DATETIME_RE = re.compile(r'((19|20|21)\d\d)[-/.]?(0[1-9]|1[012]|[1-9])[-/.]?(0[1-9]|[12][0-9]|3[01]|[1-9])([tT ]?([0-1][0-9]|2[0-3]|[1-9])([:]?([0-5][0-9]|[1-9]))?([:]([0-5][0-9]|[1-9]))?([.]([0-9])+)?)?')

# NEWLINE Token
NEWLINE    = 'NEWLINE'
NEWLINE_RE = re.compile(r'\n+|(\r\n)+')

# MSGFORMAT Token
MSGFORMAT    = 'MSGFORMAT'
MSGFORMAT_RE = re.compile(r'[A-Za-z]{3}(\d+\.\d+)')

# SEPARATORS
COMMA        = 'COMMA'
COMMA_RE     = re.compile(r',')

COLON        = 'COLON'
COLON_RE     = re.compile(r':')

MINUS        = 'MINUS'
MINUS_RE     = re.compile(r'-')

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

HELP        = 'HELP'
HELP_RE     = re.compile('HELP',re.IGNORECASE)

LAT         = 'LAT'
LAT_RE      = re.compile('LAT',re.IGNORECASE)

LON         = 'LON'
LON_RE      = re.compile('LON',re.IGNORECASE)


KEYWORDS_TOKENS = [BEGIN,STOP,TO,MSGTYPE,MSGID,EMAIL,TIME,STALIST,HELP,LAT,LON]

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
           HELP     : HELP_RE,
           LAT      : LAT_RE,
           LON      : LON_RE,
           COMMA    : COMMA_RE,
           COLON    : COLON_RE,
           MINUS    : MINUS_RE,
           NEWLINE  : NEWLINE_RE,
         }

# key ordered to optimize pattern matching
# it also defines the pattern matching rule precedence
TOKENS_ORDERED = [DATETIME]  + KEYWORDS_TOKENS + [MSGFORMAT,ID,NUMBER,COMMA,COLON,MINUS,NEWLINE]

# Literals to ignore
IGNORED_LITERALS = " \f\t\x0c"

# ENDMARKER Token to signal end of program
ENDMARKER = "ENDMARKER"


class IMSTokenizer(object):
    """ 
       Tokenizer for IMS2.0 messages.
    """
    
    # Class members
    c_log = logging.getLogger("query.IMSTokenizer")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        
        self._io_prog  = None
        
        # current parsed line
        self._line_num = -1
        
        # current position in the line
        self._pos      = -1
        
        # current token
        self._tok      = None
        
    def set_io_prog(self,a_io_prog):
        
        self._io_prog  = a_io_prog
        self._line_num = 0
        self._pos      = 0
        self._tok      = 0
        
    def io_prog(self):
        return self._io_prog
    
    def _get_ID_type(self,a_value):
        """ get the type for a particular free form ID.
            There are 3 different kinds of IDs: 
            - WCID. WildCard ID. if a_value contains a *.
            - DATA. Data in a data message. If len(a_value) > 50 bytes (or chars) and if a_value contains -
            - ID. All the rest 
        
            Args:
               a_value: the a_value
               
            Returns:
               return the found type (WCID or ID or DATA)
        
            Raises:
               None
        """
        #p = re.search('[-/=+\<\>\(\)]',a_value)
        #if p:
        #    print("MATCHED %s for %s\n"%(p,a_value))
        #if len(a_value) > 50 or (a_value.find('-') >= 0):
        if len(a_value) > 50 or re.search('[-/=+\<\>\(\)]',a_value):
            return 'DATA'
        elif a_value.find('*') >= 0:
            return 'WCID'     
        else:
            return 'ID'
    
        
        
    def tokenize(self,a_starting_pos=0):
        """ Use a generator to return an iterator on the tokens stream.
            Calling twice the tokenize method will reset the generator and the 
            position on the read stream. You can position the "cursor" on the
            read stream to the desired offset with a_starting_pos
        
            Args:
               a_starting_pos:Where to position the offset on the read stream.
                              If a_starting_pos is None, do not reset the stream position
               
            Returns:
               return next found token 
        
            Raises:
               exception LexerError if no specified Token found
        """
        
        # position 0 in io stream
        if a_starting_pos != None:
            self._io_prog.seek(a_starting_pos)
        
        for line in self._io_prog:
            #print("line to read=[%s].len(line)=%d\n"%(line,len(line)))
            
            self._line_num    += 1
        
            self._pos, max = 0, len(line)
        
            while self._pos < max:
            
                b_found = False
                # This code provides some short-circuit code for whitespace, tabs, and other ignored characters
                if line[self._pos] in IGNORED_LITERALS:
                    self._pos += 1
                    continue
            
                #print("Try to match from [%s]\n"%(line[pos:]))
                        
                for key in TOKENS_ORDERED:
                    regexp = TOKENS[key]
                    match  = regexp.match(line,self._pos)
                    if match:
                       
                        val        = match.group()
                        start, end = self._pos,(self._pos+len(val)-1)
                        
                        # when it is an ID check if this is a WCID
                        if key == 'ID':
                            type = self._get_ID_type(val)
                        else:
                            type = key
                        
                        self._tok = Token(type,val,start,end,self._line_num,line)
                    
                        #update pos
                        self._pos = end +1
                    
                        #print("Token = %s\n"%(self._tok))
                        b_found = True
                    
                        #return token using yield and generator
                        yield self._tok
                        
                        #found on so quit for loop
                        break
            
            
                if not b_found:
                    raise LexerError(self._line_num,line,self._pos)            
        
        # All lines have been read return ENDMARKER Token
        self._tok = ENDMARKERToken(self._line_num)
        yield self._tok
        
    def advance_until(self,a_tokens_expression):
        """ 
            Advance in the stream of tokens until one of the desired tokens is found.
            
            Args:
               a_tokens_expression: this is list of possible tokens to match
              
        
            Returns:
               return the matched token
        """
    
    def current_token(self):
        """ 
            return the latest consumed token.
        
            Returns:
               return the latest consumed token. None if there is no token
        """
        return self._tok
              
# unit tests part
import unittest
class TestTokenizer(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def ztestTokenizerIterator(self):     
        
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
    
    def ztestMyTest(self):
        
        next_five_days = next_day(6)
        cpt = 0
        for day in next_five_days:
            print day
            cpt +=1
            if cpt == 4:
                break
        
        print("new days")
        next_five_days = next_day(6)
        for day in next_five_days:
            print day
        
            
    def testTokenizerNext(self):
        
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("34543 342\n2009.05.04     Toto")
        
        io_prog.seek(0)
        
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        for tok in tokenizer.tokenize():
            cpt +=1
            print("Token = %s\n"%(tok))
            if cpt == 4:
                break
        
        print("restart\n")
        
        cpt = 0
        for tok in tokenizer.tokenize():
            cpt +=1
            print("Token = %s\n"%(tok))
            if cpt == 4:
                break
        
        #gen_tok = tokenizer.tokenize("val")
        
        #print("dir(gen_tok)=%s\n"%(dir(gen_tok)))
        
        #print("gen_tok.next() = %s\n"%(gen_tok.next()))
        
        #print("gen_tok.next() = %s\n"%(gen_tok.next()))
        
        #print("gen_tok.next() = %s\n"%(gen_tok.next()))
        
        #gen_tok2 = tokenizer.tokenize("val1")
        
        #print("gen_tok2.next() = %s\n"%(gen_tok2.next()))
        
        #print("gen_tok2.next() = %s\n"%(gen_tok2.next()))
    
   
import datetime
def next_day(days):
    current_day = datetime.datetime.today()
    while days:
        next_day = current_day + datetime.timedelta(days=1)
        current_day = next_day
        days -= 1
        yield next_day

   


        
        
        