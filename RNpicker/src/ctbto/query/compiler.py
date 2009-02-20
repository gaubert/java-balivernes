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
        
        for expr in self._criteria:
            s += expr.get_execution_tree()
        
        return "( criteria %s )"%(s)

class ItemAssignementStatement(Statement):
    
    def __init__(self):
        
        super(Statement,self).__init__()
        
        self._variable   = None
        self._index      = None
        self._expression = None 
        
    def add_variable(self,a_variable):
        
        self._variable = a_variable
    
    def add_index(self,a_index):
        
        self._index = a_index
    
    def add_expression(self,a_expr):
        
        self._expression = a_index    
        
    def get_execution_tree(self):
        
        s = ""
        
        for expr in self._criteria:
            s += expr.get_execution_tree()
        
        return "( assign ( var %s ) ( index %s ) ( expr %s)"%(s)
    
class ContainerBaseStatement(Statement):
    
    def __init__(self):
        
        super(ContainerBaseStatement,self).__init__()
        
        self._type        = None
        self._value       = None
        self._format      = None
    
    def add_type(self,a_type):
        
        self._type         = a_type
    
    def add_value(self,a_value):
        
        self._value = a_value
        
    def add_format(self,a_format):
        
        self._format = a_format
        
 
class DestinationStatement(ContainerBaseStatement):
 
    def __init__(self):
        
        super(DestinationStatement,self).__init__()
        
    def get_execution_tree(self):
        
        return "( to ( type %s ) ( val %s ) ( format %s ) )"%(self._type,self._value,self._format) if (self._format != None) else "( to ( type %s ) ( val %s ) )"%(self._type,self._value) 

class OriginStatement(ContainerBaseStatement):
 
    def __init__(self):
        
        super(OriginStatement,self).__init__()
        
    def get_execution_tree(self):
        return "( from ( type %s ) ( val %s ) ( format %s ) )"%(self._type,self._value,self._format) if (self._format != None) else "( from ( type %s ) ( val %s ) )"%(self._type,self._value)     
     
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
                    raise ParsingError("Error expected a STRING type but instead got %s with type %s"%(token.value,token.type))
            elif token.value == 'format':
                 # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                # if should be a name
                if token.type == 'NAME':
                    statement.add_format(token.value)
                else:
                    raise ParsingError("Error expected a NAME type but instead got %s with type %s"%(token.value,token.type))
            elif token.value != ',':
                raise ParsingError("Error expected a file or format parameter but instead got %s with type %s"%(token.value,token.type))
            
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
                    raise ParsingError("Error expected a STRING type but instead got %s with type %s"%(token.value,token.type))
            elif token.value == 'format':
                 # next token and look for =
                self._tokenizer.next()
                token = self._tokenizer.consume_token('=')
                
                # if should be a name
                if token.type == 'NAME':
                    statement.add_format(token.value)
                else:
                    raise ParsingError("Error expected a NAME type but instead got %s with type %s"%(token.value,token.type))
            elif token.value != ',':
                raise ParsingError("Error expected a file or format parameter but instead got %s with type %s"%(token.value,token.type))
            
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
            raise ParsingError("Error in parsing. non expected token %s in line %s, col %s"%(token.value,token.begin[1],token.begin[0])) 
        
        return statements
        
        
        
        
        
# unit tests part
import unittest
class TestCompiler(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def ztestTokenizerCompiler(self):
        
        c = Compiler()
        
        # need support for time => date=20081002to20081102 or date=20081002,20081024,20081212
        """
           radionuclide products :  bulletins         data             observations
                                    
                                     RRR,ARR,SSREB     sampml           particulate, noble gas
        """
        program = c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] with techno = radionuclide and mda < 10 and category > 2")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
    
    def ztestExpressionWithTO(self):
        
        c = Compiler()
        
        # need support for time => date=20081002to20081102 or date=20081002,20081024,20081212
        """
           radionuclide products :  bulletins         data             observations
                                    
                                     RRR,ARR,SSREB     sampml           particulate, noble gas
        """
        program = c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] with techno = radionuclide and mda < 10 and category > 2 to file='/tmp/data/data.bin'")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
    
    def ztestExpressionWithFrom(self):
        
        c = Compiler()
        
        # need support for time => date=20081002to20081102 or date=20081002,20081024,20081212
        """
           radionuclide products :  bulletins         data             observations
                                    
                                     RRR,ARR,SSREB     sampml           particulate, noble gas
        """
        program = c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] with techno = radionuclide and mda < 10 and category > 2 from file='/tmp/data/data.bin'")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
    
    def testExpressionWithFromAndTo(self):
        
        c = Compiler()
        
        # need support for time => date=20081002to20081102 or date=20081002,20081024,20081212
        """
           radionuclide products :  bulletins         data             observations
                                    
                                     RRR,ARR,SSREB     sampml           particulate, noble gas
        """
        #program = c.compile("retrieve spectrum[CURR,BK], analysis[CURR,BK] with techno = radionuclide , mda < 10 and category > 2 from file='/tmp/data/data.bin' to file='/tmp/to_file.data',format=SAMPML")
        
        program = c.compile("retrieve spectrum[CURR] with tech = radionuclide , mda < 10")
     
        print "get_execution_tree program %s\n"%(program.get_execution_tree())
   
        
        
        
        
        
        
        
        
        
        