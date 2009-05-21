'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org

'''
import logging
import StringIO
import copy


from ims_tokenizer import IMSTokenizer, Token, ENDMARKERToken

class ParsingError(Exception):
    """Base class for All exceptions"""
    
    c_STANDARD_ERROR_MSG = "Next keyword should be %s but instead was '%s' (keyword type %s)"
    
    @classmethod
    def create_std_error_msg(cls, a_user_friendly_keyword, a_token):
        """ 
           Create the standard Error message.
           
           Args:
               message: the message to parse
               
            Returns:
               return 
        
            Raises:
               exception
           
        """
        return cls.c_STANDARD_ERROR_MSG % (a_user_friendly_keyword, a_token.value, a_token.type)
    
    def __init__(self, a_msg, a_suggestion, a_token):
        
        self._msg        = a_msg
        self._token      = a_token
        self._suggestion = a_suggestion
        
        if a_token == None:
            extra = "" 
        else:
            # manage the endmarker case if token.begin = -1
            extra = "Error[line=%s,pos=%s]:"% (self._token.line_num, self._token.begin if (self._token.begin != -1) else 'EOF')
        
        super(ParsingError, self).__init__("%s %s."% (extra, a_msg))
    
    @property
    def instrumented_line(self):
        """ return the line with a cursor on the error """
        line = self._token.parsed_line
        
        instrumented_line  = line[:self._token.begin] + "[ERR]=>" + line[self._token.begin:] 
        return instrumented_line   

    @property
    def suggestion(self):
        """ return suggestion """
        return self._suggestion

class IMSParser(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.IMSParser")
    c_log.setLevel(logging.DEBUG)
    
    c_SHI_PRODUCTS = [Token.BULLETIN,   Token.ARRIVAL, Token.WAVEFORM, Token.EVENT, Token.ORIGIN, Token.SLSD, Token.CHANNEL, Token.STASTATUS, \
                      Token.CHANSTATUS, Token.OUTAGE, Token.RESPONSE, Token.COMMENT, Token.COMMSTATUS, Token.EXECSUM, Token.STATION]
    
    # rad products + Help
    c_RAD_PRODUCTS = [Token.ARR, Token.RRR, Token.BLANKPHD, Token.SPHDF, Token.SPHDP, Token.CALIBPHD, Token.QCPHD, Token.DETBKPHD, Token.GASBKPHD, Token.RLR, \
                      Token.HELP, Token.RMSSOH, Token.RNPS, Token.MET, Token.NETWORK, Token.SSREB, ]
    
    c_ALL_PRODUCTS = c_SHI_PRODUCTS + c_RAD_PRODUCTS
    
    c_PRODUCT      = 'PRODUCT'
    
    def __init__(self):
        """ constructor """
        
        self._tokenizer = IMSTokenizer()
        
        # io stream
        self._io_prog   = None
    
    def parse(self, message):
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
        result_dict = self._parse_header_message()
        
        # 3 choices from there: data, request or subscription message
        req_type = result_dict[Token.MSGTYPE]
        
        if   req_type == 'request':
            result_dict.update(self._parse_request_message())
        elif req_type == 'subscription':
            result_dict.update(self._parse_subscription_message())
        elif req_type == 'data':
            result_dict.update(self._parse_data_message())
        else:
            raise ParsingError("unknown request type %s. contact the NMS administrator.\n"%(req_type), None, self._tokenizer.current_token())
        
        return result_dict
    
    def _parse_header_message(self):
        """ Read the 4 first lines that are considered as the "header of the message".
            This will help finding the message type
        
            Args: None
               
            Returns:
               return a dictionary of parsed values 
        
            Raises:
               exception 
        """ 
        result = {}
        
        # might need to advance until a BEGIN token
        # for the moment check if the first token is a begin
        token = self._tokenizer.next()
        
        # look for line 1 BEGIN message_format
        # format: begin message_format
        if token.type != Token.BEGIN:
            raise ParsingError(ParsingError.create_std_error_msg('a begin', token), 'The begin line is missing or not well formatted', token)
    
        token = self._tokenizer.next()
        
        # look for a message_format
        if token.type != Token.MSGFORMAT:
            raise ParsingError(ParsingError.create_std_error_msg('a msg format id (ex:ims2.0)', token), 'The begin line is not well formatted', token)
            
        result[Token.MSGFORMAT] = token.value.lower()
        
        #eat next line characters
        token = self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        # line 2: get the message type
        # format: msg_type request
        if token.type != Token.MSGTYPE:
            raise ParsingError(ParsingError.create_std_error_msg('a msg_type', token), 'The msg_type id line is missing', token)
            
        token = self._tokenizer.next()
        
        if token.type != Token.ID:
            raise ParsingError(ParsingError.create_std_error_msg('a id', token), 'The msg_type id is missing or the msg_type line is mal-formated', token)
        
        result[Token.MSGTYPE] = token.value.lower()
         
        #eat next line characters
        token = self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        # line 3: get the message id
        # format: msg_id id_string [source]
        if token.type != Token.MSGID:
            raise ParsingError(ParsingError.create_std_error_msg('a msg_id', token), 'The msg_id line is missing', token)
            
        token = self._tokenizer.next()
        
        # next token is an ID 
        # TODO: the id_string should be up to 20 characters and should not contains blanks or \
        if token.type not in (Token.ID, Token.NUMBER):
            raise ParsingError(ParsingError.create_std_error_msg('an id', token), 'The msg_id line is missing the id or is not well formatted', token)
        result[Token.MSGID] = token.value
        
        token = self._tokenizer.next()
        
        # it can be a source or a NEWLINE
        
        # this is a source and source format 3-letter country code followed by _ndc (ex: any_ndc)
        if token.type in (Token.ID, Token.EMAILADDR):
            result['SOURCE'] = token.value 
            
            # go to next token
            self._tokenizer.next()
                     
        elif token.type != Token.NEWLINE:
            raise ParsingError(ParsingError.create_std_error_msg('a newline or a source', token), 'The msg_id line is not well formatted', token)
        
        #eat current and next line characters
        token = self._tokenizer.consume_while_current_token_is_in([Token.NEWLINE])
        
        #optional line 4: it could now be the optional REF_ID
        if token.type == Token.REFID:
            result['REFID'] = self._parse_ref_id_line()
            token = self._tokenizer.current_token()
            
        # line 4 or 5: e-mail foo.bar@domain_name
        # look for an EMAIL keyword
        if token.type != Token.EMAIL:
            raise ParsingError(ParsingError.create_std_error_msg('an email', token), 'The email line is probably missing or misplaced', token)
    
        token = self._tokenizer.next()
        # look for the EMAILADDR
        if token.type != Token.EMAILADDR: 
            raise ParsingError(ParsingError.create_std_error_msg('an email address', token), 'The email address might be missing or is malformated', token)
           
        result[Token.EMAIL] = token.value.lower()
        
        #eat next line characters
        self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        return result
    
    def _parse_ref_id_line(self):
        """ Parse a ref_id line
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        result_dict = {}
        
        token = self._tokenizer.next()
        
        if token.type not in (Token.ID, Token.NUMBER):
            raise ParsingError(ParsingError.create_std_error_msg('an id', token), 'The ref_id line is missing a ref_src or it is not well formatted', token)
         
        result_dict['REFSTR'] = token.value
        
        token = self._tokenizer.next()
        
        # could be the optional ref_src
        if token.type in (Token.ID, Token.NUMBER):
            result_dict['REFSRC'] = token.value
            token = self._tokenizer.next()
        
        # now the [part seq_num [of tot_num]]
        if token.type == Token.PART:
            
            #get the seq num val
            token = self._tokenizer.next()
            
            if token.type not in (Token.ID, Token.NUMBER):
                raise ParsingError(ParsingError.create_std_error_msg('an id', token), "The ref_id line is missing a the seq_num in the \'part\' construct: ref_id ref_str [ref_src] [part seq_num [of tot_num]]", token)
            
            result_dict['SEQNUM'] = token.value
            
            # look for OF token
            token = self._tokenizer.next()
            
            if token.type == Token.OF:
                
                # get the tot_num val
                token = self._tokenizer.next()
                
                if token.type not in (Token.ID, Token.NUMBER):
                    raise ParsingError(ParsingError.create_std_error_msg('an id', token), "The ref_id line is missing a the tot_num in the \'of\' construct: ref_id ref_str [ref_src] [part seq_num [of tot_num]]", token)
            
                result_dict['TOTNUM'] = token.value
                
                #go to next
                token = self._tokenizer.next()
        # it can then only be a new line
        elif token.type != Token.NEWLINE:
            raise ParsingError(ParsingError.create_std_error_msg('an id, a part or a new line ', token), "The ref_id line is mal formatted. It should follow ref_id ref_str [ref_src] [part seq_num [of tot_num]]", token)
             
        #eat current and next line characters
        self._tokenizer.consume_while_current_token_is_in([Token.NEWLINE])
        
        return result_dict
           
    def _parse_request_message(self):
        """ Parse Radionuclide and SHI request messages
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        result_dict = {}
        
        cpt = 1
        
        # each product is in a dictionary
        product_name              = 'PRODUCT_%d'% (cpt)
        result_dict[product_name] = {}
        product = result_dict[product_name]
        
        token = self._tokenizer.current_token()
        
        # add already seen keywords in this list. This is used to handle product "inheritance"
        seen_keywords = []
        
        # For the moment look for the different possible tokens
        while token.type != Token.STOP and token.type != Token.ENDMARKER:
            
            # if the current token has already be seen
            # store the new product and create a new one with the same properties as the current one
            # product kind of inherit properties from the previous one
        
            # if it is a product use c_PRODUCT marker
            s_type = IMSParser.c_PRODUCT if (token.type in IMSParser.c_ALL_PRODUCTS) else token.type
            if s_type in seen_keywords:
                cpt += 1
                product_name  = 'PRODUCT_%d'% (cpt)
                result_dict[product_name] = copy.deepcopy(product)
                product = result_dict[product_name]
                
                # clean seen_keyword
                seen_keywords = []
            
            # time keyword
            if token.type == Token.TIME:
               
                product.update(self._parse_time())
                
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(Token.TIME)
                   
            # bull_type 
            # they both expect an ID
            elif token.type == Token.BULLTYPE:
                      
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(Token.BULLTYPE) 
                  
                # next token should be a ID (Bulletin type)
                token = self._tokenizer.next()
                
                if token.type != Token.ID:
                    raise ParsingError(ParsingError.create_std_error_msg('a id', token), 'The bull_type id qualifying type of bulletin requested is missing', token)

                product[Token.BULLTYPE] = token.value
                
                self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
            #RELATIVE_TO origin | event | bulletin or ID
            elif token.type == Token.RELATIVETO:
               
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(Token.RELATIVETO)
               
                # next token should be a ID (Bulletin type)
                token = self._tokenizer.consume_next_tokens([Token.ORIGIN, Token.EVENT, Token.BULLETIN, Token.ID])
                
                product[Token.RELATIVETO] = token.value

                self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])   
                                 
            # mag keyword
            elif token.type == Token.MAG:
               
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(Token.MAG)
                
                product.update(self._parse_mag()) 
                
            #DEPTH
            elif token.type == Token.DEPTH:
                 
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(Token.DEPTH)
                
                product.update(self._parse_depth())
                         
            #LAT or LON
            elif token.type in (Token.LAT,Token.LON):
                
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(token.type)
                
                product.update(self._parse_latlon(token.type))
            
            # parse complex products
            elif token.type in IMSParser.c_SHI_PRODUCTS:
                
                # to handle multiple product retrievals
                # need to add all PRODUCTS
                seen_keywords.append(IMSParser.c_PRODUCT)
                
                product.update(self._parse_complex_product(token))
            
            elif token.type in IMSParser.c_RAD_PRODUCTS:
                
                # to handle multiple product retrievals
                # need to add all PRODUCTS
                seen_keywords.append(IMSParser.c_PRODUCT)
                
                product.update(self._parse_complex_product(token))
                        
            elif token.type == Token.STALIST or token.type == Token.CHANLIST:
                
                # to handle multiple product retrievals
                # need to add all PRODUCTS
                seen_keywords.append(token.type)
                                
                product.update(self._parse_list(token))
                                      
            else:
                raise ParsingError('Unknown keyword %s (keyword type %s)' % (token.value, token.type), 'Request mal-formatted', token)

            # eat any left NEWLINE token
            token = self._tokenizer.consume_while_current_token_is_in([Token.NEWLINE])
            
        # check if we have a stop
        if token.type != Token.STOP:
            raise ParsingError('End of request reached without encountering a stop keyword', 'Stop keyword missing or truncated request', token)
        
        return result_dict
    
    def _parse_list(self, a_token):
        """ Parse a station list or a channel list.
            It should be a mag range mag [date1[time1]] to [date2[time2]]
        
            Args: a_token: The token that defines the type (STALIST or CHANLIST)
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        res_dict = {}
        
        type = a_token.type
        
        list = []
        
        while True:
            
            token = self._tokenizer.next() 
        
            #should find an ID
            if token.type == Token.ID or token.type == Token.WCID:
            
                list.append(token.value)
                
                # should find a COMMA or NEWLINE
                # IF COMMA loop again else leave loop
                token = self._tokenizer.consume_next_tokens([Token.COMMA, Token.NEWLINE])
                
                if token.type == Token.NEWLINE:
                    #leave the loop
                    break
            else:
                raise ParsingError(ParsingError.create_std_error_msg('a list id', token), 'The list line is not well formatted', token)
  
        # if goes here then there is something in stations
        res_dict[type] = list
        
        return res_dict  
    
    def _parse_simple_product(self, a_token):
        """ Parse simple products.
            These products don't have any parameters like a format and subformat.
            
            Args: a_token: the current token
            
        """ 
        res_dict = {}
        
        # get product type
        res_dict['TYPE'] = a_token.type
        
        # expect nothing else but NEWLINES
        self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        return res_dict
            
    def _parse_complex_product(self, a_token):
        """ Parse complex products either SHI or Radionuclide
            Args: a_token: token
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """
        res_dict = {}
        
        # get product type
        res_dict['TYPE'] = a_token.type
        
        token = self._tokenizer.next()
        
        if token.type == Token.NEWLINE:
            return res_dict
        
        # first try to consume the SUBTYPE if there is any
        # in that case, there is a subtype (only for SLSD and arrivals)
        elif token.type == Token.COLON:
            
            token = self._tokenizer.consume_next_token(Token.ID)
            res_dict['SUBTYPE'] = token.value
            
            # go to next token
            token = self._tokenizer.next()
        
        #if we have a new line our job is over 
        if token.type == Token.NEWLINE:
            return res_dict
        
        if token.type == Token.MSGFORMAT:
            res_dict['FORMAT'] = token.value
            
            #get the next token
            token = self._tokenizer.next()
            
            # if this is a COLON then there is a subformat
            if token.type == Token.COLON:
                token = self._tokenizer.next()
                if token.type == Token.ID:
                    
                    res_dict['SUBFORMAT'] = token.value
                    
                    #consume next NEWLINE token
                    self._tokenizer.consume_next_token(Token.NEWLINE)
                else:
                    raise ParsingError(ParsingError.create_std_error_msg('a subformat value', token), 'The product line [product_type format[:subformat]] (ex:waveform ims2.0:cm6) is not well formatted', token)
            # it could be a NEWLINE and there is no subformat
            elif token.type != Token.NEWLINE:
                raise ParsingError(ParsingError.create_std_error_msg('a subformat value or a new line', token), 'The subformat or format part of the product line [product_type format:[subformat]] (ex:waveform ims2.0:cm6) is not well formatted', token)
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a newline or a msg format (ex:ims2.0)', token), 'The product line [product_type format[:subformat]] (ex:waveform ims2.0:cm6) is not well formatted', token)
            
        return res_dict  
            
    
    def _parse_mag(self):
        """ Parse magnitude component.
            It should be a mag range mag [date1[time1]] to [date2[time2]]
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """  
        res_dict = {}
        
        token = self._tokenizer.next()
        
        if token.type == Token.NUMBER:
            
            res_dict['STARTMAG'] = token.value
            
            # try to consume the next token that should be TO
            self._tokenizer.consume_next_token(Token.TO)
            
        elif token.type == Token.TO:
            # add the min value because begin value has been omitted
            res_dict['STARTMAG'] = Token.MIN 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or to', token), 'The mag line is not well formatted', token)
            
        token = self._tokenizer.next()
        
        # it can be either NUMBER (ENDMAG) or NEWLINE (this means that it will magnitude max)
        if token.type == Token.NUMBER:
            res_dict['ENDMAG'] = token.value
            
            #consume new line
            self._tokenizer.consume_next_token(Token.NEWLINE)
            
        elif token.type == Token.NEWLINE:
            
            res_dict['ENDMAG'] = Token.MAX 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or newline', token), 'The mag line is not well formatted', token)
        
        #go to next token
        self._tokenizer.next()
       
        return res_dict
        
    def _parse_depth(self):
        """ Parse depth component.
            It should be a depth range depth [shallow] to [deep]
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """
        res_dict = {}
        
        token = self._tokenizer.next()
        
        if token.type == Token.NUMBER:
            
            res_dict['STARTDEPTH'] = token.value
            
            # try to consume the next token that should be TO
            self._tokenizer.consume_next_token(Token.TO)
            
        elif token.type == Token.TO:
            # add the min value because begin value has been omitted
            res_dict['STARTDEPTH'] = Token.MIN 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or to', token), 'The depth line is not well formatted', token)
            
        token = self._tokenizer.next()
        
        # it can be either NUMBER (ENDMAG) or NEWLINE (this means that it will magnitude max)
        if token.type == Token.NUMBER:
            res_dict['ENDDEPTH'] = token.value
            
            #consume new line
            self._tokenizer.consume_next_token(Token.NEWLINE)
            
        elif token.type == Token.NEWLINE:
            
            res_dict['ENDDEPTH'] = Token.MAX 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or newline', token), 'The depth line is not well formatted', token)
        
        #go to next token
        self._tokenizer.next()
       
        return res_dict
        
    def _parse_latlon(self, a_type):
        """ Parse latlon component.
            It should be a lat range lat [min] to [max]
        
            Args: a_type : LAT or LON
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """
        res_dict = {}
        
        token = self._tokenizer.next()
        
        # negative number
        if token.type == Token.MINUS:
            
            #expect a number
            token = self._tokenizer.consume_next_token(Token.NUMBER)
            
            res_dict['START%s' % (a_type)] = '-%s' % (token.value)
            
            # try to consume the next token that should be TO
            self._tokenizer.consume_next_token(Token.TO)
        # positive number
        elif token.type == Token.NUMBER:
            
            res_dict['START%s' % (a_type)] = token.value
            
            # try to consume the next token that should be TO
            self._tokenizer.consume_next_token(Token.TO)
        # no min value    
        elif token.type == Token.TO:
            # add the min value because begin value has been omitted
            res_dict['START%s' % (a_type)] = Token.MIN 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or to', token), 'The lat or lon line is not well formatted', token)
            
        token = self._tokenizer.next()
        
        # it can be either NUMBER (ENDMAG) or NEWLINE (this means that it will magnitude max)
        if   token.type == Token.MINUS:
            
            #expect a number
            token = self._tokenizer.consume_next_token(Token.NUMBER)
            
            res_dict['END%s' % (a_type)] = '-%s'% (token.value)
            
            # try to consume the next token that should be TO
            #go to next token
            self._tokenizer.next()
            
        elif token.type == Token.NUMBER:
            
            res_dict['END%s' % (a_type)] = token.value
            
            #consume new line
            self._tokenizer.consume_next_token(Token.NEWLINE)
            
        elif token.type == Token.NEWLINE:
            
            res_dict['END%s' % (a_type)] = Token.MAX 
        else:
            raise ParsingError(ParsingError.create_std_error_msg('a number or to', token), 'The lat or lon line is not well formatted', token)
            
        #go to next token
        self._tokenizer.next()
       
        return res_dict
            
    def _parse_time(self):
        """ Parse time component.
            It should be a time range time [date1[time1]] to [date2[time2]]
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """
        time_dict = {}
        
        token = self._tokenizer.next()
        
        if token.type != Token.DATETIME:
            raise ParsingError(ParsingError.create_std_error_msg('a datetime', token), 'The time line is incorrect. The datetime value is probably malformatted or missing.', token)
            
        time_dict['STARTDATE'] = token.value
        
        token = self._tokenizer.next()
        # it should be a TO
        if token.type != Token.TO:
            raise ParsingError(ParsingError.create_std_error_msg('a to', token), 'The to keyword is missing in the line time', token)
            
        token = self._tokenizer.next()
        if token.type != Token.DATETIME:
            raise ParsingError(ParsingError.create_std_error_msg('a datetime', token), 'The time line is incorrect. The datetime value is probably malformatted or missing.', token)
            
        time_dict['ENDDATE'] = token.value
        
        #consume at least a NEWLINE
        self._tokenizer.consume_next_token(Token.NEWLINE)
        
        return time_dict
    
    def _parse_subscription_message(self):
        """ Parse Radionuclide and SHI request messages
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        raise ParsingError("_parse_subscription_message is currently not implemented", ENDMARKERToken(100))
    
    def _parse_data_message(self):
        """ Parse Radionuclide and SHI request messages
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        raise ParsingError("_parse_data_message is currently not implemented", ENDMARKERToken(100))
       