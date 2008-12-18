 
""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging

from tokenizer import Tokenizer


class Statement(object):
    """Base Class used for all statements """
    
    def execute(self):
        raise Error(-1,"Abstract method to be implemented by the children")
    
class BlockStatement(Statement):
    
    def __init__(self):
        
        super(Statement,self).__init__()
        
        self._statements = []
        
    def add(self,statement):
        
        #precondition, check that the passed object is a statement
        self._statements.append(statement)
        
    def execute(self):
        last = None
        
        for statement in self._statements:
            last = statement.execute()
       
        
        return last;

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
        self._tokenizer = Tokenizer(program)
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
        
    
    def _read_statements(self):
        
        token
        
        
        