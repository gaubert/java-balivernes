 
""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging

from tokenizer import Tokenizer

class ParsingError(Exception):
    """Base class for All exceptions"""

    def __init__(self,a_msg):
        super(ParsingError,self).__init__(a_msg)
        

class Statement(object):
    """Base Class used for all statements """
    
    def execute(self):
        raise Error(-1,"Abstract method to be implemented by the children")
    
class BlockStatement(Statement):
    
    def __init__(self):
        
        super(BlockStatement,self).__init__()
        
        self._statements = []
        
    def add(self,statement):
        
        #precondition, check that the passed object is a statement
        self._statements.append(statement)
        
    def execute(self):
        last = None
        
        for statement in self._statements:
            last = statement.execute()
       
        return last

class RetrieveStatement(Statement):
    
    def __init__(self):
        
        super(RetrieveStatement,self).__init__()
        
        self._statements = []
        
    def add(self,statement):
        
        #precondition, check that the passed object is a statement
        self._statements.append(statement)
        
    def execute(self):
        last = None
        
        for statement in self._statements:
            last = statement.execute()
       
        return last

class Compiler(object):
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
        self._compile()
        
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
        
    
    def _read_retrieve_statement(self):
        """ private compilation method .
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        # look for a filter statement s[a,v,b] , t[a,b,c]
        # for retrieve spectrum[CURR,BK], analysis[CURR,BK] where
        # we want to have (retrieve ( filter ( [ (literal spectrum) (literal CURR) ) ([ (literal analysis) (literal BK) ) ) 
        filter_dict = {}
        
        token = self._tokenizer.next()
        
        while token.value != 'where':
            if token.type == 'NAME':
                filter_name = token
                token = self._tokenizer.next()
                token = self._tokenizer.consume_token('[') 
                filter_values = []
                while token.value != ']':    
                    if token.type == 'NAME':
                        filter_values.append(token)
                        token = self._tokenizer.next()
                    elif token.type == 'OP' and token.value == ',':
                        token = self._tokenizer.next()
                    else:
                        raise ParsingError("Error expected a filter value but found %s with type %s"%(token.value,token.type))
                #consume ] to be sure
                token = self._tokenizer.consume_token(']') 
                filter_dict[filter_name] = filter_values
                        
                        
            else:
                raise ParsingError("Error expected a filter name but found %s with type %s"%(token.value,token.type))
            
        
       
    
    
    def _read_statements(self):
        """ read statements.
        
            Args:
              
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        token = self._tokenizer.current_token()
        
        if token.value.lower() == 'retrieve':
            return self._read_retrieve_statement()
        else:
            raise ParsingError("Error in parsing. non expected token %s in line %s, col %s"%(token.value,token.begin[1],token.begin[0])) 
        
        
        
        
        
        
        
        
# unit tests part
import unittest
class TestCompiler(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testTokenizerCompiler(self):
        
        c = Compiler()
        
        c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] where techno = radionuclide")
     
   
        
        
        
        
        
        
        
        
        
        