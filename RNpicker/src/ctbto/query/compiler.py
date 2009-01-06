""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging

from tokenizer import Tokenizer
from expr_compiler import ExpressionCompiler

class ParsingError(Exception):
    """Base class for All exceptions"""

    def __init__(self,a_msg):
        super(ParsingError,self).__init__(a_msg)
        

class Statement(object):
    """Base Class used for all statements """
    
    def execute(self):
        raise Error(-1,"Abstract method to be implemented by the children")
    
    def get_execution_tree(self):
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
    
    def get_execution_tree(self):
        last = None
        
        for statement in self._statements:
            last = statement.get_execution_tree()
       
        return last

class CriteriaStatement(Statement):
    
    def __init__(self):
        
        super(CriteriaStatement,self).__init__()
        
        self._criteria = []
        
    def add_criteria(self,expr):
        
        self._criteria.append(expr)
        
        
    def get_execution_tree(self):
        
        s = ""
        
        for (op,a,b) in self._criteria:
            s += "( %s ( literal %s ) (literal %s ) )"%(op,a,b)
        
        return "( criteria %s )"%(s)
        
class FilterStatement(Statement):
 
    def __init__(self):
        
        super(FilterStatement,self).__init__()
        
        self._filters = {}
        
    def add_filter(self,name,values):
        
        if name not in self._filters:
            self._filters[name] = values
        else:
            raise ParsingError("Error filter %s already exists"%(name))
        
    def get_execution_tree(self):
        s = ""
        
        for (key,value) in self._filters.iteritems():
            s += "( [ ( literal %s )"%(key)
            for v in value:
                s += " ( literal %s )"%(v)
            s += " ) "
        
        return "( filter %s)"%(s)
        
class RetrieveStatement(Statement):
    
    def __init__(self):
        
        super(RetrieveStatement,self).__init__()
        
        self._statements = []
        
    def add(self,statement):
        
        #precondition, check that the passed object is a statement
        self._statements.append(statement)
        
    def get_execution_tree(self):
        last = ""
        
        for statement in self._statements:
            last += statement.get_execution_tree()
       
        return "( retrieve %s )"%(last)

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
        
        while token.type != 'ENDMARKER':
            expr = self._expr_compiler.compile(self._tokenizer)
            print "expr = %s\n"%(expr)
            statement.add_criteria(expr)
            
            token = self._tokenizer.current_token()
                
        
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
        # look for a filter statement s[a,v,b] , t[a,b,c] until where
        # for retrieve spectrum[CURR,BK], analysis[CURR,BK] where
        # we want to have (retrieve ( filter ( [ (literal spectrum) (literal CURR) ) ([ (literal analysis) (literal BK) ) )  
        token = self._tokenizer.next()
        
        while token.value != 'where':
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
                        raise ParsingError("Error expected a filter value but found %s with type %s"%(token.value,token.type))
                #consume ] to be sure
                token = self._tokenizer.consume_token(']')  
                statement.add_filter(filter_name,filter_values)
                
            elif token.type == 'OP' and token.value == ',':
                #comma consume next token
                token = self._tokenizer.consume_token(',')           
            else:
                raise ParsingError("Error expected a filter name but found %s with type %s"%(token.value,token.type))
            
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
       
        # consume the where token
        self._tokenizer.consume_token('where') 
        
        # read criteria statements
        ret_statement.add(self._read_criteria_statement())
        
        # read criteria statement
        # look for where min(spectrum.A) , date = "20081203/20081205", date="20081203/to/20091203"
        # => parse expression, parse date (in date parse period, parse list of date, parse single dates)
        
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
            raise ParsingError("Error in parsing. non expected token %s in line %s, col %s"%(token.value,token.begin[1],token.begin[0])) 
        
        return statements
        
        
        
        
        
# unit tests part
import unittest
class TestCompiler(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testTokenizerCompiler(self):
        
        c = Compiler()
        
        program = c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] where techno = radionuclide and magnitude < 10")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
   
        
        
        
        
        
        
        
        
        
        