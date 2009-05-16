'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org

'''
import logging
from tokenizer import Tokenizer
from expr_compiler import ExpressionCompiler


class IMSParser(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.compiler")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        
        self._tokenizer = None

        # the current statement used to create a pseudo iterator
        self._current_statement = None
        
        #use delegation
        self._expr_compiler = ExpressionCompiler()
 
    def compile(self,program):
        """ compile the passed program.
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        self._tokenizer = Tokenizer()
        self._tokenizer.tokenize(program)
        self._tokenizer.next()
        
        return self._compile()
        
    def _compile(self):
        """ private compilation method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        # need to add a block statement for the future
        block = BlockStatement()
        
        for s in self._read_statements():
            block.add(s)
        
        return block
    
    def _read_criteria_statement(self):
        """ private compilation method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """
        statement = CriteriaStatement() 
        
        token = self._tokenizer.current_token()
        
        # Can have a destination or origin statement or nothing
        while token.type != 'ENDMARKER':
            
            expr = self._expr_compiler.compile(self._tokenizer)
            print "expr = %s\n"%(expr)
            statement.add_criteria(expr)
            
            token = self._tokenizer.current_token()
            # if find to or from there is a destination or origin statement
            if token.value == 'to' or token.value == 'from':
                break
                
        return statement
    
    def _read_destination_statement(self):
        """ destination statement. This is where to store the data.
        
            Args:
               None
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        statement = DestinationStatement()
        token = self._tokenizer.current_token()
        
        # after a destination statement, it is possible to have 
        while True:
            
            if token.type == 'ENDMARKER' or token.value == 'from':
                # leave loop 
                break
            # for the moment look for file or format
            elif token.value == 'file':
                
                statement.add_type(token.value)
                
                # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                if token.type == 'STRING':
                    statement.add_value(token.value)
                else:
                    raise ParsingError("Expected a STRING type but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            elif token.value == 'format':
                 # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                # if should be a name
                if token.type == 'NAME':
                    statement.add_format(token.value)
                else:
                    raise ParsingError("Expected a NAME type but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            elif token.value != ',':
                raise ParsingError("Expected a file or format parameter but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            
            # in case we have , do nothing eat it
            
            #get next token
            token = self._tokenizer.next()
        
        return statement
    
    def _read_origin_statement(self):
        """ origin statement. This is where to read the data.
        
            Args:
               None
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        statement = OriginStatement()
        token = self._tokenizer.current_token()
        
        # after a destination statement, it is possible to have 
        while True:
            
            if token.type == 'ENDMARKER' or token.value == 'to':
                # leave loop 
                break
            # for the moment look for file or format
            elif token.value == 'file':
                
                statement.add_type(token.value)
                
                # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                if token.type == 'STRING':
                    statement.add_value(token.value)
                else:
                    raise ParsingError("Expected a STRING type but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            elif token.value == 'format':
                 # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                # if should be a name
                if token.type == 'NAME':
                    statement.add_format(token.value)
                else:
                    raise ParsingError("Expected a NAME type but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            elif token.value != ',':
                raise ParsingError("Expected a file or format parameter but instead got %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            
            # in case we have , do nothing eat it
            
            #get next token
            token = self._tokenizer.next()
        
        return statement
    
    def _read_filter_statement(self):
        """ private compilation method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        statement = FilterStatement()
        # look for a filter statement s[a,v,b] , t[a,b,c] until with
        # for retrieve spectrum[CURR,BK], analysis[CURR,BK] where
        # we want to have (retrieve ( filter ( [ (literal spectrum) (literal CURR) ) ([ (literal analysis) (literal BK) ) )  
        token = self._tokenizer.next()
        
        while token.value != 'with':
            if token.type == 'NAME':
                filter_name = token.value
                token = self._tokenizer.next()
                token = self._tokenizer.consume_token('[') 
                filter_values = []
                while token.value != ']':    
                    if token.type == 'NAME' or token.type == 'NUMBER':
                        filter_values.append(token.value)
                        token = self._tokenizer.next()
                    elif token.type == 'OP' and token.value == ',':
                        token = self._tokenizer.next()
                    else:
                        raise ParsingError("Expected a filter value but instead found %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
                #consume ] to be sure
                token = self._tokenizer.consume_token(']')  
                statement.add_filter(filter_name,filter_values)
                
            elif token.type == 'OP' and token.value == ',':
                #comma consume next token
                token = self._tokenizer.consume_token(',')           
            else:
                raise ParsingError("Expected a filter name but instead found %s with type %s"%(token.value,token.type),token.begin[1],token.begin[0])
            
        return statement
    
    def _read_retrieve_statement(self):
        """ private compilation method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        ret_statement = RetrieveStatement()
        
        # first read a 'filter' statement
        ret_statement.add(self._read_filter_statement())
       
        # consume the with token
        self._tokenizer.consume_token('with') 
        
        # read criteria statements
        ret_statement.add(self._read_criteria_statement())
        
        # read criteria statement
        # look for with min(spectrum.A) , date = "20081203/20081205", date="20081203/to/20091203"
        # => parse expression, parse date (in date parse period, parse list of date, parse single dates)
        
        # if current_token 
        token = self._tokenizer.current_token()
        
        #look for to or from construct
        while token.type != 'ENDMARKER':
            if token.value == 'to':
                # consume the token
                self._tokenizer.consume_token('to')
                # look for destination
                ret_statement.add(self._read_destination_statement())
            
            if token.value == 'from':
                # consume the token
                self._tokenizer.consume_token('from')
                # look for destination
                ret_statement.add(self._read_origin_statement())
                
            #update token variable
            token = self._tokenizer.current_token()
        
        return ret_statement
    
    
    def _read_statements(self):
        """ read statements.
        
            Args:
              
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        statements = []
        
        token = self._tokenizer.current_token()
        
        if token.value.lower() == 'retrieve':
            statements.append(self._read_retrieve_statement())
        else:
            raise ParsingError("Non expected token %s"%(token.value),token.begin[1],token.begin[0]) 
        
        return statements
        
        
# unit tests part
import unittest
class TestIMSParser(unittest.TestCase):
    
    TOKENIZER_TEST_1 = "begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop"
    
    def setUp(self):
         
        print " setup \n"
        
    def testTokenizeTest(self):
        """ Test the tokenizer and see how it would behave for IMS2.0 messages"""
         
          # get simple string
        tokens = Tokenizer()
        
        #tokens.tokenize("retrieve spectrum[CURR,BK] where technology = radionuclide and id=123456 in file=\"/tmp/ctbto.data\", filetype=SAMPML")
        
        tokens.tokenize(TestIMSParser.TOKENIZER_TEST_1)
        
        #valuesToCheck = ['retrieve','i','>','3','']
        i = 0
         
        for tok in tokens: 
            print "token = %s"%(tok.value) 
            #self.assertEqual(valuesToCheck[i],tok.value)
            i +=1
    
    def ztestTokenizerCompiler(self):
        
        c = IMSParser()
        
        # need support for time => date=20081002to20081102 or date=20081002,20081024,20081212
        program = c.compile("begin ims2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
    