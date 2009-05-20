'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org

'''
import logging
import StringIO
import copy


from ims_tokenizer import IMSTokenizer, Token

class ParsingError(Exception):
    """Base class for All exceptions"""

    def __init__(self, a_msg, a_line_num=None, a_pos=None):
        
        self._line_num = a_line_num
        self._pos      = a_pos
        
        if self._line_num == None and self._pos == None:
            extra = "" 
        else:
            extra = "(line=%s,pos=%s)"% (self._line_num, self._pos)
        
        super(ParsingError, self).__init__("%s %s."% (a_msg, extra))
    
    #def __str__(self):
    #    return "ParsingError (line:%s,col:%s) => %s"%()
        

class IMSParser(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.IMSParser")
    c_log.setLevel(logging.DEBUG)
    
    c_PRODUCTS = [Token.BULLETIN, Token.SLSD, Token.ARRIVAL, Token.WAVEFORM]
    
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
            raise ParsingError("unknown request type %s. contact the NMS administrator.\n"%(req_type))
        
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
            raise ParsingError("Expected the message to start with a BEGIN type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        token = self._tokenizer.next()
        
        # look for a message_format
        if token.type != Token.MSGFORMAT:
            raise ParsingError("Expected a MSGFORMAT type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        result[Token.MSGFORMAT] = token.value
        
        #eat next line characters
        token = self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        # line 2: get the message type
        # format: msg_type request
        if token.type != Token.MSGTYPE:
            raise ParsingError("Expected a MSGTYPE type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        token = self._tokenizer.next()
        
        if token.type != Token.ID:
            raise ParsingError("Expected a ID type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        result[Token.MSGTYPE] = token.value
         
        #eat next line characters
        token = self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        # line 3: get the message id
        # format: msg_id id_string [source]
        if token.type != Token.MSGID:
            raise ParsingError("Expected a MSGID type but instead got [%s] with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        token = self._tokenizer.next()
        
        # next token is an ID 
        # TODO: the id_string should be up to 20 characters and should not contains blanks or \
        if token.type != Token.ID and token.type != Token.NUMBER:
            raise ParsingError("Expected a ID type but instead got [%s] with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        result[Token.MSGID] = token.value
        
        token = self._tokenizer.next()
        
        # it can be a source or a NEWLINE
        
        # this is a source and source format 3-letter country code followed by _ndc (ex: any_ndc)
        if token.type == Token.ID:
            result['SOURCE'] = token.value 
            
            # go to next token
            self._tokenizer.next()
                     
        elif token.type != Token.NEWLINE:
            raise ParsingError("Expected an ID type as the source or a NEWLINE type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        #eat current and next line characters
        token = self._tokenizer.consume_while_current_token_is_in([Token.NEWLINE])
        
        # line 4: e-mail foo.bar@domain_name
        # look for an EMAIL keyword
        if token.type != Token.EMAIL:
            raise ParsingError("Expected a EMAIL type but instead got [%s] with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        token = self._tokenizer.next()
        # look for the EMAILADDR
        if token.type != Token.EMAILADDR:
            raise ParsingError("Expected an EMAILADDR type but instead got [%s] with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        result[Token.EMAIL] = token.value
        
        #eat next line characters
        self._tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        return result
           
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
        while token.type != Token.STOP:
            
            # if the current token has already be seen
            # store the new product and create a new one with the same properties as the current one
            # product kind of inherit properties from the previous one
            if token.type in seen_keywords:
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
                    raise ParsingError("Expected a ID type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)

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
            elif token.type == Token.LAT or token.type == Token.LON:
                
                # to handle multiple product retrievals
                # add current token type in seen_keywords
                seen_keywords.append(token.type)
                
                product.update(self._parse_latlon(token.type))
            
            elif token.type == Token.BULLETIN or token.type == Token.SLSD or token.type == Token.ARRIVAL or token.type == Token.WAVEFORM:
                
                # to handle multiple product retrievals
                # need to add all PRODUCTS
                seen_keywords.extend(IMSParser.c_PRODUCTS)
                
                product.update(self._parse_shi_product(token))
                        
            elif token.type == Token.STALIST:
                                
                product.update(self._parse_sta_list())
                
                # to handle multiple product retrievals
                # need to add all PRODUCTS
                seen_keywords.append(Token.STALIST)
                                     
            else:
                raise ParsingError("Was not expecting a token with type %s and value %s"% (token.value, token.type), token.line_num, token.begin)  
           
            # eat any left NEWLINE token
            token = self._tokenizer.consume_while_current_token_is_in([Token.NEWLINE])
        
        return result_dict
    
    def _parse_sta_list(self):
        """ Parse a station list.
            It should be a mag range mag [date1[time1]] to [date2[time2]]
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        res_dict = {}
        
        stations = []
        
        while True:
            
            token = self._tokenizer.next() 
        
            #should find an ID
            if token.type == Token.ID:
            
                stations.append(token.value)
                
                # should find a COMMA or NEWLINE
                # IF COMMA loop again else leave loop
                token = self._tokenizer.consume_next_tokens([Token.COMMA, Token.NEWLINE])
                
                if token.type == Token.NEWLINE:
                    #leave the loop
                    break
            else:
                raise ParsingError("Expected a ID type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        # if goes here then there is something in stations
        res_dict[Token.STALIST] = stations
        
        return res_dict   
            
    def _parse_shi_product(self, a_token):
        """ Parse shi product.
            It should be a mag range mag [date1[time1]] to [date2[time2]]
        
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
                    raise ParsingError("Was expecting a subformat value (token type = ID), instead got %s with type %s "% (token.value, token.type), token.line_num, token.begin)
            # it could be a NEWLINE and there is no subformat
            elif token.type != Token.NEWLINE:
                raise ParsingError("Expected a NEWLINE or ID type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        else:
            ParsingError("Expected a NEWLINE, MSGFORMAT but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
            
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
            ParsingError("Expected a NUMBER or TO type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
         
        token = self._tokenizer.next()
        
        # it can be either NUMBER (ENDMAG) or NEWLINE (this means that it will magnitude max)
        if token.type == Token.NUMBER:
            res_dict['ENDMAG'] = token.value
            
            #consume new line
            self._tokenizer.consume_next_token(Token.NEWLINE)
            
        elif token.type == Token.NEWLINE:
            
            res_dict['ENDMAG'] = Token.MAX 
        
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
            ParsingError("Expected a NUMBER or TO type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
         
        token = self._tokenizer.next()
        
        # it can be either NUMBER (ENDMAG) or NEWLINE (this means that it will magnitude max)
        if token.type == Token.NUMBER:
            res_dict['ENDDEPTH'] = token.value
            
            #consume new line
            self._tokenizer.consume_next_token(Token.NEWLINE)
            
        elif token.type == Token.NEWLINE:
            
            res_dict['ENDDEPTH'] = Token.MAX 
        
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
            ParsingError("Expected a NUMBER or TO type but instead got %s with type %s" % (token.value, token.type), token.line_num, token.begin)
         
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
            raise ParsingError("Expected a DATETIME type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        time_dict['STARTDATE'] = token.value
        
        token = self._tokenizer.next()
        # it should be a TO
        if token.type != Token.TO:
            raise ParsingError("Expected a TO type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
        token = self._tokenizer.next()
        if token.type != Token.DATETIME:
            raise ParsingError("Expected a DATETIME type but instead got %s with type %s"% (token.value, token.type), token.line_num, token.begin)
        
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
        raise ParsingError("_parse_subscription_message is currently not implemented")
    
    def _parse_data_message(self):
        """ Parse Radionuclide and SHI request messages
        
            Args: None
               
            Returns:
               return a dictionary of pased values 
        
            Raises:
               exception 
        """ 
        raise ParsingError("_parse_data_message is currently not implemented")
       