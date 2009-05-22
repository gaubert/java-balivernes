'''
Created on May 16, 2009

@author: guillaume.aubert@ctbto.org
'''

import logging
import re

class LexerError(Exception):
    """LexerError Class"""
    
    def __init__(self,a_msg):
        
        super(LexerError,self).__init__(a_msg)
        

class IllegalCharacterError(LexerError):
    """IllegalCharacterError Class"""

    def __init__(self, a_line_num, a_line, a_pos):
        
        self._line     = a_line
        self._pos      = a_pos
        self._line_num = a_line_num
        
        instrumented_line  = a_line[:a_pos] + "(ERR)=>" + a_line[a_pos:]
        
        msg = "Illegal Character %s in Line %d, position %d.[%s]"% (a_line[a_pos], a_line_num, a_pos, instrumented_line)
        
        super(IllegalCharacterError, self).__init__(msg)
        
    @property    
    def line(self):
        """ line accessor """ 
        return self._line
    
    @property
    def line_num(self):
        """ line_num accessor """
        return self._line_num
    
    @property
    def pos(self):
        """ pos accessor """
        return self._pos
    
    def illegal_character(self):
        return self._line[self._pos]

class BadTokenError(LexerError):
    
    def __init__(self, a_line_num, a_line, a_pos, a_expected_token_types, a_found_token):
         
        self._line     = a_line
        self._pos      = a_pos
        self._line_num = a_line_num
         
        msg = "Found Token with type %s and value [%s] in Line %s, position %s. Was expecting %s."% (a_found_token.type,a_found_token.value,a_line_num,a_pos,a_expected_token_types)

        super(BadTokenError, self).__init__(msg)
         
    @property    
    def line(self):
        """ line accessor """
        return self._line
    
    @property
    def line_num(self):
        """ line_num accessor """
        return self._line_num
    
    @property
    def pos(self):
        """ pos accessor """
        return self._pos
         
         
class NonExistingTokenError(LexerError):
    pass

class TokensNotFoundError(LexerError):
    pass

class Token(object):
    
    ID            = 'ID'
    DATA          = 'DATA'
    WCID          = 'WCID'
    EMAILADDR     = 'EMAILADDR'
    DATETIME      = 'DATETIME'
    NUMBER        = 'NUMBER'
    NEWLINE       = 'NEWLINE'
    MSGFORMAT     = 'MSGFORMAT'
    COMMA         = 'COMMA'
    COLON         = 'COLON'
    MINUS         = 'MINUS'
    BEGIN         = 'BEGIN'
    STOP          = 'STOP'
    TO            = 'TO'
    OF            = 'OF'
    PART          = 'PART'
    MSGTYPE       = 'MSGTYPE'
    REFID         = 'REFID'
    MSGID         = 'MSGID'
    PRODID        = 'PRODID'
    EMAIL         = 'EMAIL'
    TIME          = 'TIME'
    STALIST       = 'STALIST'
    BULLTYPE      = 'BULLTYPE'
    DEPTH         = 'DEPTH'
    MAG           = 'MAG'
    MAGTYPE       = 'MAGTYPE'
    CHANLIST      = 'CHANLIST'
    RELATIVETO    = 'RELATIVETO'
    HELP          = 'HELP'
    LAT           = 'LAT'
    LON           = 'LON'
    # ENDMARKER Token to signal end of program
    ENDMARKER     = 'ENDMARKER'
    MAX           = 'MAX'
    MIN           = 'MIN'
    # waveform products
    BULLETIN       = 'BULLETIN'
    WAVEFORM       = 'WAVEFORM'
    EVENT          = 'EVENT'
    ORIGIN         = 'ORIGIN'
    EXECSUM        = 'EXECSUM'
    SLSD           = 'SLSD'
    ARRIVAL        = 'ARRIVAL'
    OUTAGE         = 'OUTAGE'
    STASTATUS      = 'STASTATUS'
    CHANSTATUS     = 'CHANSTATUS'
    CHANNEL        = 'CHANNEL'
    WAVEMISSION    = 'WAVEMISSION'
    WAVEQUALITY    = 'WAVEQUALITY'
    STATION        = 'STATION'
    COMMSTATUS     = 'COMM_STATUS'
    COMMENT        = 'COMMENT'
    RESPONSE       = 'RESPONSE'
    
    # radionuclide prodcuts
    DETBKPHD       = 'DETBKPHD'
    BLANKPHD       = 'BLANKPHD'
    CALIBPHD       = 'CALIBPHD'
    GASBKPHD       = 'GASBKPHD'
    QCPHD          = 'QCPHD'
    SPHDP          = 'SPHDP'
    SPHDF          = 'SPHDF'
    ARR            = 'ARR'
    RRR            = 'RRR'
    RLR            = 'RLR'
    SSREB          = 'SSREB'
    ALERTFLOW      = 'ALERTFLOW'
    ALERTSYSTEM    = 'ALERTSYSTEM'
    ALERTTEMP      = 'ALERTTEMP'
    ALERTUPS       = 'ALERTUPS'
    MET            = 'MET'
    RNPS           = 'RNPS'
    NETWORK        = 'NETWORK'
    RMSSOH         = 'RMSSOH'
    
    #deprecated
    ARMR           = 'ARMR'
    FPEB           = 'FPEB'
    
         
    def __init__(self, type, value, begin, end, line_num, parsed_line, file_pos=-1):
        
        self._type         = type
        self._value        = value
        self._begin        = begin
        self._end          = end
        self._parsed_line  = parsed_line
        self._line_num     = line_num
        self._file_pos     = file_pos
    
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
    def file_pos(self):
        """ Return file_pos """
        return self._file_pos
    
    @property
    def parsed_line(self):
        """ Return the token line """
        return self._parsed_line
    
    @property
    def line_num(self):
        """ return the line number """
        return self._line_num
    
    def __repr__(self):
        return "Token[type=%s,value={%s},line_num=%s,(begin index,end index)=(%s,%s)"% (self._type, self._value, self._line_num, self._begin, self._end)  

class ENDMARKERToken(Token):
    """ A very special Token: ENDMARKER to signal the end of program """
    
    def __init__(self, a_line_num):
        
        super(ENDMARKERToken, self).__init__(Token.ENDMARKER, None, -1, -1, a_line_num, "")

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
        return "ENDMARKER Token line_num = %d"% (self._line_num)  


# functor tools to assemble tokens
def group(*choices)   : return '(' + '|'.join(choices) + ')'
def any(*choices)     : return group(*choices) + '*'
def maybe(*choices)   : return group(*choices) + '?'


# All the regular expr for the different tokens

# NUMBER
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
# ID 
ID_RE       = re.compile(r'[/\*A-Za-z_\+=\(\)\<\>]([\w]|[/=\<\>\(\)\.@\*\+-])*')

# DATETIME regexpr
DATETIME_RE = re.compile(r'((19|20|21)\d\d)[-/.]?(0[1-9]|1[012]|[1-9])[-/.]?(0[1-9]|[12][0-9]|3[01]|[1-9])([tT ]?([0-1][0-9]|2[0-3]|[0-9])([:]?([0-5][0-9]|[0-9]))?([:]([0-5][0-9]|[1-9]))?([.]([0-9])+)?)?')

# EMAIL Address regexpr as defined in RFC 2822 (do not support square brackets and double quotes)
EMAILADDR_RE = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",re.IGNORECASE)
 

# NEWLINE Token
NEWLINE_RE = re.compile(r'\n+|(\r\n)+')

# MSGFORMAT
MSGFORMAT_RE = re.compile(r'[A-Za-z]{3}(\d+\.\d+)')

# SEPARATORS
COMMA_RE     = re.compile(r',')

COLON_RE     = re.compile(r':')

MINUS_RE     = re.compile(r'-')

# Language keywords

# BEGIN 
BEGIN_RE      = re.compile('BEGIN', re.IGNORECASE)
# STOP
STOP_RE       = re.compile('STOP', re.IGNORECASE)
# TO
TO_RE         = re.compile('TO', re.IGNORECASE)
# OF
OF_RE         = re.compile('OF', re.IGNORECASE)
# PART
PART_RE         = re.compile('PART', re.IGNORECASE)
# MSGTYPE
MSGTYPE_RE    = re.compile('MSG_TYPE', re.IGNORECASE)
# MSGID
MSGID_RE      = re.compile('MSG_ID', re.IGNORECASE)
# PRODID
PRODID_RE     = re.compile('PROD_ID', re.IGNORECASE)
# REFID
REFID_RE      = re.compile('REF_ID', re.IGNORECASE)
# EMAIL
EMAIL_RE      = re.compile('E-MAIL', re.IGNORECASE)
# TIME
TIME_RE       = re.compile('TIME', re.IGNORECASE)
# STALIST
STALIST_RE    = re.compile('STA_LIST', re.IGNORECASE)
# BULL_TYPE
BULLTYPE_RE   = re.compile('BULL_TYPE', re.IGNORECASE)
# DEPTH
DEPTH_RE      = re.compile('DEPTH', re.IGNORECASE)
# MAG
MAG_RE        = re.compile('MAG', re.IGNORECASE)
#MAGTYPE
MAGTYPE_RE    = re.compile('MAG_TYPE', re.IGNORECASE)
#CHANLIST
CHANLIST_RE   = re.compile('CHAN_LIST', re.IGNORECASE)
#RELATIVE_TO
RELATIVETO_RE = re.compile('RELATIVE_TO', re.IGNORECASE)
# HELP
HELP_RE       = re.compile('HELP', re.IGNORECASE)
# LAT
LAT_RE        = re.compile('LAT', re.IGNORECASE)
# LON
LON_RE        = re.compile('LON', re.IGNORECASE)

KEYWORDS_TOKENS = [Token.BEGIN, Token.STOP, Token.TO, Token.OF, Token.PART, Token.MSGTYPE, Token.MSGID, Token.REFID, Token.EMAIL, \
                   Token.TIME,  Token.STALIST, Token.BULLTYPE, Token.DEPTH, Token.MAG, Token.MAGTYPE, Token.CHANLIST, \
                   Token.RELATIVETO, Token.HELP, Token.LAT, Token.LON,Token.PRODID]

# products

#BULLETIN
BULLETIN_RE      = re.compile('BULLETIN', re.IGNORECASE)
#WAVEFORM
WAVEFORM_RE      = re.compile('WAVEFORM', re.IGNORECASE)
#SLSD
SLSD_RE          = re.compile('SLSD', re.IGNORECASE)
# ARRIVAL
ARRIVAL_RE       = re.compile('ARRIVAL', re.IGNORECASE)
#STA_STATUS
STA_STATUS_RE    = re.compile('STA_STATUS', re.IGNORECASE)
#CHAN_STATUS
CHAN_STATUS_RE   = re.compile('CHAN_STATUS', re.IGNORECASE)
#CHANNEL
CHANNEL_RE       = re.compile('CHANNEL', re.IGNORECASE)
#WAVE_MISSION
WAVE_MISSION_RE  = re.compile('WAVE_MISSION', re.IGNORECASE)
#WAVE_QUALITY
WAVE_QUALITY_RE  = re.compile('WAVE_QUALITY', re.IGNORECASE)
#STATION
STATION_RE       = re.compile('STATION', re.IGNORECASE)
#EVENT
EVENT_RE         = re.compile('EVENT', re.IGNORECASE)
#EXECSUM
EXECSUM_RE       = re.compile('EXECSUM', re.IGNORECASE)
#COMMENT
COMMENT_RE       = re.compile('COMMENT', re.IGNORECASE)
#COMM_STATUS
COMM_STATUS      = re.compile('COMM_STATUS', re.IGNORECASE)
#ORIGIN
ORIGIN_RE        = re.compile('ORIGIN', re.IGNORECASE)
#OUTAGE
OUTAGE_RE        = re.compile('OUTAGE', re.IGNORECASE)
#RESPONSE
RESPONSE_RE      = re.compile('RESPONSE', re.IGNORECASE)

#DETBKPHD
DETBKPHD_RE      = re.compile('DETBKPHD', re.IGNORECASE)
#GASBKPHD
GASBKPHD_RE      = re.compile('GASBKPHD', re.IGNORECASE)
#BLANKPHD
BLANKPHD_RE      = re.compile('BLANKPHD', re.IGNORECASE)
#CALIBPHD
CALIBPHD_RE      = re.compile('CALIBPHD', re.IGNORECASE)
#QCPHD
QCPHD_RE         = re.compile('QCPHD', re.IGNORECASE)
#SPHDP
SPHDP_RE         = re.compile('SPHDP', re.IGNORECASE)
#SPHDF
SPHDF_RE         = re.compile('SPHDF', re.IGNORECASE)
#RLR
RLR_RE           = re.compile('RLR', re.IGNORECASE)
#ARR
ARR_RE           = re.compile('ARR', re.IGNORECASE)
#ARR
RRR_RE           = re.compile('RRR', re.IGNORECASE)
#ALERTFLOW
ALERTFLOW_RE     = re.compile('ALERT_FLOW', re.IGNORECASE)
#ALERT_SYSTEM
ALERTSYSTEM_RE   = re.compile('ALERT_SYSTEM', re.IGNORECASE)
#ALERT_TEMP
ALERTTEMP_RE     = re.compile('ALERT_TEMP', re.IGNORECASE)
#ALERT_TEMP
ALERTUPS_RE      = re.compile('ALERT_UPS', re.IGNORECASE)
#MET
MET_RE           = re.compile('MET', re.IGNORECASE)
#RNPS
RNPS_RE          = re.compile('RNPS', re.IGNORECASE)
#SSREB
SSREB_RE         = re.compile('SSREB', re.IGNORECASE)
#NETWORK
NETWORK_RE       = re.compile('NETWORK', re.IGNORECASE)
#RMSSOH
RMSSOH_RE        = re.compile('RMSSOH', re.IGNORECASE)

#Deprecated ?
#ARMR
ARMR_RE          = re.compile('ARMR', re.IGNORECASE)
#FPEB
FPEB_RE          = re.compile('FPEB', re.IGNORECASE)

SHI_PRODUCTS_TOKENS   = [Token.BULLETIN, Token.WAVEFORM, Token.SLSD, Token.ARRIVAL, Token.EVENT, Token.ORIGIN, Token.EXECSUM, \
                         Token.OUTAGE, Token.RESPONSE, Token.STASTATUS, Token.CHANSTATUS, Token.CHANNEL, Token.WAVEMISSION, \
                         Token.WAVEQUALITY, Token.STATION, Token.COMMENT, Token.COMMSTATUS]

RADIO_PRODUCTS_TOKENS = [Token.DETBKPHD, Token.BLANKPHD, Token.CALIBPHD, Token.QCPHD, Token.SPHDP, Token.SPHDF, Token.GASBKPHD, \
                         Token.ARR, Token.RRR, Token.SSREB, Token.RLR, Token.RNPS, Token.ALERTFLOW, Token.ALERTSYSTEM, \
                         Token.ALERTTEMP, Token.ALERTUPS, Token.RMSSOH, Token.MET, Token.NETWORK, Token.ARMR, Token.FPEB]

TOKENS_RE = {
           Token.ID           : ID_RE,
           #different ID Flavours
           Token.WCID         : ID_RE,
           Token.DATA         : ID_RE,
           Token.EMAILADDR    : EMAILADDR_RE,
           Token.DATETIME     : DATETIME_RE,
           Token.NUMBER       : NUMBER_RE,
           Token.MSGFORMAT    : MSGFORMAT_RE,
           Token.BEGIN        : BEGIN_RE,
           Token.STOP         : STOP_RE,
           Token.TO           : TO_RE,
           Token.OF           : OF_RE,
           Token.PART         : PART_RE,
           Token.MSGTYPE      : MSGTYPE_RE,
           Token.MSGID        : MSGID_RE,
           Token.REFID        : REFID_RE,
           Token.PRODID       : PRODID_RE,
           Token.EMAIL        : EMAIL_RE,
           Token.TIME         : TIME_RE,
           Token.STALIST      : STALIST_RE,
           Token.BULLTYPE     : BULLTYPE_RE,
           Token.DEPTH        : DEPTH_RE,
           Token.MAG          : MAG_RE,
           Token.MAGTYPE      : MAGTYPE_RE,
           Token.CHANLIST     : CHANLIST_RE,
           Token.RELATIVETO   : RELATIVETO_RE,
           Token.HELP         : HELP_RE,
           Token.LAT          : LAT_RE,
           Token.LON          : LON_RE,
           
           # ID refined tokens
           #SHI products
           Token.BULLETIN     : BULLETIN_RE,
           Token.WAVEFORM     : WAVEFORM_RE,
           Token.EVENT        : EVENT_RE,
           Token.EXECSUM      : EXECSUM_RE,
           Token.SLSD         : SLSD_RE,
           Token.ARRIVAL      : ARRIVAL_RE,
           Token.STASTATUS    : STA_STATUS_RE,
           Token.CHANSTATUS   : CHAN_STATUS_RE,
           Token.CHANNEL      : CHANNEL_RE,
           Token.WAVEMISSION  : WAVE_MISSION_RE,
           Token.WAVEQUALITY  : WAVE_QUALITY_RE,
           Token.STATION      : STATION_RE, 
           Token.COMMENT      : COMMENT_RE,
           Token.COMMSTATUS   : COMM_STATUS, 
           Token.ORIGIN       : ORIGIN_RE,
           Token.OUTAGE       : OUTAGE_RE,
           Token.RESPONSE     : RESPONSE_RE,
           #radio nuclide products
           Token.DETBKPHD     : DETBKPHD_RE,
           Token.BLANKPHD     : BLANKPHD_RE,
           Token.CALIBPHD     : CALIBPHD_RE,
           Token.GASBKPHD     : GASBKPHD_RE,
           Token.QCPHD        : QCPHD_RE,
           Token.SPHDP        : SPHDP_RE,
           Token.SPHDF        : SPHDF_RE,
           Token.RLR          : RLR_RE,
           Token.ARR          : ARR_RE,
           Token.RRR          : RRR_RE,
           Token.RNPS         : RNPS_RE,
           Token.ALERTFLOW    : ALERTFLOW_RE,
           Token.ALERTSYSTEM  : ALERTSYSTEM_RE,
           Token.ALERTTEMP    : ALERTTEMP_RE,
           Token.ALERTUPS     : ALERTUPS_RE,
           Token.MET          : MET_RE,
           Token.SSREB        : SSREB_RE,
           Token.NETWORK      : NETWORK_RE,
           Token.RMSSOH       : RMSSOH_RE,
           
           Token.ARMR         : ARMR_RE,
           Token.FPEB         : FPEB_RE,
           
           Token.COMMA        : COMMA_RE,
           Token.COLON        : COLON_RE,
           Token.MINUS        : MINUS_RE,
           Token.NEWLINE      : NEWLINE_RE,
           Token.ENDMARKER    : None,
         }

# key ordered to optimize pattern matching
# it also defines the pattern matching rule precedence
TOKENS_ORDERED = [Token.DATETIME]  + KEYWORDS_TOKENS + SHI_PRODUCTS_TOKENS + RADIO_PRODUCTS_TOKENS \
                 + [Token.MSGFORMAT, Token.EMAILADDR, Token.ID, Token.NUMBER,Token.COMMA, Token.COLON, Token.MINUS, Token.NEWLINE]

# Literals to ignore
IGNORED_LITERALS = " \f\t\x0c"

class IMSTokenizer(object):
    """ 
       Tokenizer for IMS2.0 messages.
    """
    
    # Class members
    c_log = logging.getLogger("query.IMSTokenizer")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        
        self._io_prog        = None
        
        # current parsed line
        self._line_num       = -1
        
        # current position in the line
        self._line_pos       = -1
        
        # file-like offset position
        self._file_pos       = -1
        
        # file-like original position (used for have __iter__ returning always the same sequence)
        self._io_prog_offset = -1
        
        # current token
        self._tok            = None
        
        # internal generator on current stream
        # used by the iterator method
        self._gen            = None
        
    def set_io_prog(self, a_io_prog):
        """ 
           Pass the io stream to parse and start reading from where it has been positioned 
           Args:
               a_io_prog: file-like object
        """
        self._io_prog        = a_io_prog
        self._io_prog_offset = a_io_prog.tell()
        self._line_num       = 0
        self._line_pos       = 0
        self._file_pos       = -1
        self._tok            = 0
        # reset generator
        self._gen            = None
    
    def set_file_pos(self, a_file_pos):
        """ 
           Set the starting offset in the read io stream (file).
           Reset the generator as the file positio has changed.
           if a_file_pos is None then do not touch anything
           
           Args:
               a_file_pos: If a_file_pos is None then set file_pos to -1 and the stream will not be touched.
                           The generator will start reading from where it is
        """
        #special case do not touch anything and read from where we are
        self._file_pos = a_file_pos if (a_file_pos != None) else -1
        
    def file_pos(self):
        """ return the position of the reading cursor in current file """
        return self._file_pos
    
    def line_num(self):
        """ return the line_num currently read """
        return self._line_num
        
    def io_prog(self):
        """ return the io prog """
        return self._io_prog
    
    def _get_ID_type(self, a_value):
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
        if len(a_value) > 50 or re.search('[/=+\<\>\(\)]', a_value):
            return 'DATA'
        elif a_value.find('*') >= 0:
            return 'WCID'     
        else:
            return 'ID'
    
        
        
    def _create_tokenize_gen(self, a_starting_pos=-1):
        """ Use a generator to return an iterator on the tokens stream.
            Calling twice the tokenize method will reset the generator and the 
            position on the read stream. You can position the "cursor" on the
            read stream to the desired offset with a_starting_pos
        
            Args:
               a_starting_pos:Where to position the offset on the read stream.
                              If a_starting_pos is -1, do not touch the current stream
               
            Returns:
               return next found token 
        
            Raises:
               exception LexerError if no specified Token found
        """
        
        # position 0 in io stream
        if a_starting_pos != -1:
            self._io_prog.seek(a_starting_pos)
        
        for line in self._io_prog:
            #print("line to read=[%s].len(line)=%d\n"%(line,len(line)))
            
            self._line_num    += 1
        
            self._file_pos = self._io_prog.tell()
            
            self._line_pos, max = 0, len(line)
        
            while self._line_pos < max:
            
                b_found = False
                # This code provides some short-circuit code for whitespace, tabs, and other ignored characters
                if line[self._line_pos] in IGNORED_LITERALS:
                    self._line_pos += 1
                    continue
            
                #print("Try to match from [%s]\n"%(line[pos:]))
                        
                for key in TOKENS_ORDERED:
                    regexp = TOKENS_RE[key]
                    match  = regexp.match(line, self._line_pos)
                    if match:
                       
                        val        = match.group()
                        start, end = self._line_pos, (self._line_pos+len(val)-1)
                        
                        # when it is an ID check if this is a WCID
                        if key == Token.ID:
                            type = self._get_ID_type(val)
                        else:
                            type = key
                        
                        self._tok = Token(type,val, start, end, self._line_num, line,  self._file_pos)
                    
                        #update pos
                        self._line_pos = end +1
                    
                        #print("Token = %s\n"%(self._tok))
                        b_found = True
                    
                        #return token using yield and generator
                        yield self._tok
                        
                        #found on so quit for loop
                        break
            
            
                if not b_found:
                    raise IllegalCharacterError(self._line_num, line, self._line_pos)            
        
        # All lines have been read return ENDMARKER Token
        self._tok = ENDMARKERToken(self._line_num)
        yield self._tok
        
        
    def __iter__(self):
        """ 
            iterator from the begining of the stream.
            If you call twice this method the second iterator will continue to iterate from 
            where the previous one was and it will not create a new one.
            To create a you one, you have to pass the io_prog again. 
        """
        self._gen = self._create_tokenize_gen(self._file_pos)
        
        return self
        
        
    def next(self):
        """
           Return the next token
            
           Returns:
               return next found token 
        """
        
        # if no generator have been created first do it and call next
        if self._gen == None:
            self._gen = self._create_tokenize_gen(self._file_pos)
        
        return self._gen.next()
    
    def consume_next_token(self, a_token_type):
        """
           Consume the next token and check that it is the expected type otherwise send an exception
           
           Args:
               a_token_type:  the token type to consume
            
           Returns:
               return the consumed token 
           
           Raises:
               exception  BadTokenError if a Token Type that is not a_token_type is found
        """
        
        tok = self.next()
        
        if tok.type != a_token_type:
            raise BadTokenError(tok.line_num, tok.parsed_line, tok.begin, a_token_type, tok)
        else:
            return tok
        
    def consume_while_next_token_is_in(self, a_token_types_list):
        """
           Consume the next tokens as long as they have one of the passed types.
           This means that at least one token with one of the passed types needs to be matched.
           
           Args:
               a_token_types_list: the token types to consume
            
           Returns:
               return the next non matching token 
        """
        
        self.consume_next_tokens(a_token_types_list)
        
        while True:
        
            tok = self.next()
        
            if tok.type not in a_token_types_list:
                return tok
    
    def consume_while_current_token_is_in(self, a_token_types_list):
        """
           Consume the tokens starting from the current token as long as they have one of the passed types.
           It is a classical token eater. It eats tokens as long as they are the specified type
           
           Args:
               a_token_types_list: the token types to consume
            
           Returns:
               return the next non matching token 
        """
        
        tok = self.current_token()
        
        while tok.type in a_token_types_list:
            tok = self.next()
        
        return tok
        
        
    
    def consume_next_tokens(self, a_token_types_list):
        """
           Consume the one of the next token types given in the list and check that it is the expected type otherwise send an exception
            
           Args:
               a_tokens_list:  the token types to list 
               
           Returns:
               return next token 
           
           Raises:
               exception  BadTokenError if a Token Type that is not in a_token_types_list is found
        """
        
        tok = self.next()
        
        if tok.type not in a_token_types_list:
            raise BadTokenError(tok.line_num, tok.parsed_line, tok.begin, a_token_types_list, tok)
        else:
            return tok
        
        
    def advance_until(self, a_tokens_list):
        """ 
            Advance in the stream of tokens until one of the desired tokens is found.
            
            
            Args:
               a_tokens_expression: this is list of possible tokens to match.
                                    the corresponding regular expression is used to try matching the token
              
        
            Returns:
               return the matched token
        """
        # check that the list contains know tokens
        tokens_to_match        = []
        has_to_match_endmarker = False
        # last possible cursor position in the current line
        max                    = -1
        
        for tok in a_tokens_list:
            if TOKENS_RE.has_key(tok):
                # ENDMARKER needs to be differentiated
                if tok == Token.ENDMARKER:
                    has_to_match_endmarker = True
                else:
                    tokens_to_match.append(tok)
            else:
                raise NonExistingTokenError("The token named %s doesn't exist"%(tok))
             
        for line in self._io_prog: 
            self._line_num    += 1
        
            self._line_pos, max = 0, len(line)
        
            # This code provides some short-circuit code for whitespace, tabs, and other ignored characters
            if line[self._line_pos] in IGNORED_LITERALS:
                self._line_pos += 1
                continue
            
            #print("Try to match from [%s]\n"%(line[pos:]))
                        
            for key in tokens_to_match:
                regexp = TOKENS_RE[key]
                #here search anywhere in the line for the token
                match  = regexp.search(line, self._line_pos)
                if match:
                    val        = match.group()
                    start, end = self._line_pos, (self._line_pos+len(val)-1)
                     
                    # do all the tricks to return the right TOKENS (see SUB TOKENS like WCID DATA)
                        
                    # when it is an ID check if this is a WCID
                    if key == Token.ID:
                        type = self._get_ID_type(val)
                    else:
                        type = key
                        
                        self._tok = Token(type, val, start, end, self._line_num, line)
                    
                        #update pos
                        self._line_pos = end +1
                        
                        # compute file_pos and reposition the cursor to this point in the file
                        # like that the stream starts just after the last found token
                        self._file_pos += self._line_pos
                        self._io_prog.seek(self._file_pos)
                    
                        #return token (no generator)
                        return self._tok
            
            self._file_pos = self._io_prog.tell()
            # not found go to next line
                                
        
        # All lines have been read return ENDMARKER Token
        self._tok = ENDMARKERToken(self._line_num)
        self._line_pos = max
        self._file_pos = self._io_prog.tell()
        if has_to_match_endmarker:
            return self._tok
        else:
            raise TokensNotFoundError("Could not find any of the following tokens %s"%(a_tokens_list))
    
    def current_token(self):
        """ 
            return the latest consumed token.
        
            Returns:
               return the latest consumed token. None if there is no token
        """
        return self._tok
              


        
        
        