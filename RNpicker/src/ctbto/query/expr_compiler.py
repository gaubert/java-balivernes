""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging
from tokenizer import Tokenizer

def make_class(classname,dict):
    
    inst = object.__new__(classname)
        
    inst.__dict__ = dict
    
    return inst

class OperatorTypes(object):
    
    c_log = logging.getLogger("query.OperatorTypes")
    c_log.setLevel(logging.DEBUG)
    
    c_additive       = set(["+","-","&"])
    c_multiplicative = set(["*","/"])
    c_comparative    = set(["<",">","=","<=",">=","<>"])
    c_power          = set(["^","**"])
    c_or             = set(["or","||"])
    c_and            = set(["and","&&"])
    
    c_type = {
              "add":c_additive,
              "mul":c_multiplicative,
              "comp":c_comparative,
              "pow":c_power,
              "or":c_or,
              "and":c_and
             }
    
    def __init__(self):
        """ constructor """
    
    def check(self,what,where):
        
        if where not in OperatorTypes.c_type.keys():
            return False
        
        for s in OperatorTypes.c_type[where]:
            if what.value == s:
                return True
        
        return False
        
    def is_additive(self,op):
        return self.check(op,"add")
    
    def is_multiplicative(self,op):
        return self.check(op,"mul")
    
    def is_comparative(self,op):
        return self.check(op,"comp")
    
    def is_power(self,op):
        return self.check(op,"pow")
    
    def is_disjunction(self,op):
        return self.check(op,"or")

    def is_conjunction(self,op):
        return self.check(op,"and")
    
# add executor factory => see if it is necessary
class Executor(object):
    
    # Class members
    c_log = logging.getLogger("query.Executor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        
        # the operation
        self._op = op
    
    def initialize(self,argument):
        #default do nothing
        return
    
    # abstract method list of values
    def execute(self,values):
        raise Exception("Error. need to be redefined in children")

class NumberBinopExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.NumberBinopExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(NumberBinopExecutor,self).__init__(op)
     
    def execute(self,values):  
        
        # more or less than 2 elements => error
        if len(values) != 2:
            raise Exception("Error. A BinOp Operation has two and only two arguments. Passed values = %s\n"%(values))
        
        return self._op.compute(values[0],values[1]) 

class NumberExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.NumberExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(NumberExecutor,self).__init__(op)
        
    def initialize(self,op):
        self._value = op.get_value()
     
    def execute(self,values):  
        return self._value
    
class Expression(object):
    """ the expression object => heart of the system
    """
    
    # Class members
    c_log = logging.getLogger("query.Expression")
    c_log.setLevel(logging.DEBUG)
    
    c_priority = {"or":1,"and":2,"test":3,"sum":4,"prod":5,"power":6,"unop":7,"atom":8}
    
    c_types = [type(None),type("string"),type(1),type(1.0)]
    
    c_executor_dispatcher = {
                              "%number:none":NumberExecutor,
                              "%string:none":"StringExecutor",
                              "%number:number:number":NumberBinopExecutor
                             
                            }
    
    """
        dispatch.put("%number:null", NumberExecutor.class);
        dispatch.put("%string:null", StringExecutor.class);
        dispatch.put("%ident:null", IdentExecutor.class);
        dispatch.put("%index:...", IndexExecutor.class);
        dispatch.put("%date:null", DateExecutor.class);
        dispatch.put("list:...", ListExecutor.class);
        dispatch.put("hash:...", HashExecutor.class);
        dispatch.put("count:...", CountExecutor.class);

        // Some math stuff
        dispatch.put("sqrt:number", Sqrt.class);
        dispatch.put("cos:number",  Cos.class);
        dispatch.put("sin:number",  Sin.class);
        dispatch.put("tan:number",  Tan.class);
        dispatch.put("log:number",  Log.class);
        dispatch.put("log10:number",  Log10.class);
        dispatch.put("exp:number",  Exp.class);
        dispatch.put("acos:number",  Acos.class);
        dispatch.put("asin:number",  Asin.class);
        dispatch.put("atan:number",  Atan.class);
        dispatch.put("abs:number",  Abs.class);
        dispatch.put("sgn:number",  Sgn.class);

        dispatch.put("ceil:number",  Ceil.class);
        dispatch.put("floor:number",  Floor.class);
        dispatch.put("round:number",  Round.class);

        dispatch.put("min:number:number",  Min.class);
        dispatch.put("max:number:number",  Max.class);
        dispatch.put("atan2:number:number",  Atan2.class);

        dispatch.put("add:hash:hash", MergeHashExecutor.class);
        dispatch.put("merge:hash:hash", MergeHashExecutor.class);
        dispatch.put("add:list:list", MergeListExecutor.class);
        dispatch.put("merge:list:list", MergeListExecutor.class);

        dispatch.put("eq:list:list", EQListExecutor.class);

        // Mars compute
        dispatch.put("add:...", RemoteBinOpExecutor.class);
        dispatch.put("sub:...", RemoteBinOpExecutor.class);
        dispatch.put("mul:...", RemoteBinOpExecutor.class);
        dispatch.put("div:...", RemoteBinOpExecutor.class);

        dispatch.put("pow:...", RemoteBinOpExecutor.class);

        dispatch.put("eq:...",  RemoteBinOpExecutor.class);
        dispatch.put("ne:...",  RemoteBinOpExecutor.class);
        dispatch.put("lt:...",  RemoteBinOpExecutor.class);
        dispatch.put("le:...",  RemoteBinOpExecutor.class);
        dispatch.put("gt:...",  RemoteBinOpExecutor.class);
        dispatch.put("ge:...",  RemoteBinOpExecutor.class);

        dispatch.put("neg:...", RemoteUnOpExecutor.class);
        dispatch.put("not:...", RemoteUnOpExecutor.class);

        // builtins
        dispatch.put("save:...", SaveExecutor.class);
        dispatch.put("print:...", PrintExecutor.class);
        dispatch.put("assert:...", AssertExecutor.class);
        dispatch.put("sort:list", SortExecutor.class);
    """
    
    def __init__(self):
        """ constructor """
        
        # list of children
        self._children = []
        
    
    def add(self,child):
        """ add child in the expression """
        self._children.append(child)
    
    def _make_executor(self,expr,values):
        """ executor factory """
        
        name      = expr.get_name()
        signature = "%s"%(name) 
        
        if len(values) == 0:
            signature += ":none"
        else:
            for value in values:
                if  type(value)  == Expression.c_types[0]:
                    #None
                    signature += ":none"
                elif type(value) == Expression.c_types[1]:
                    #string
                    signature += ":string"
                elif type(value) == Expression.c_types[2]: 
                    # int
                    signature  += ":number"
                elif type(value) == Expression.c_types[3]:
                    # float 
                    signature += ":number"
        
        classname = Expression.c_executor_dispatcher.get(signature,None)
        
        if classname == None:
            raise Exception("Error cannot find the right dispatch for %s"%(signature))
        
        executor = make_class(classname,{'_op':expr})
        
        executor.initialize(expr)
       
        return executor
        
        
    def evaluate(self):
        """ evaluate the expr => execute it """
        values = []
        
        # for each child in the children list
        for expr in self._children:
            v = expr.evaluate()
            values.append(v)
        
        executor = self._make_executor(self,values)
        
        result = executor.execute(values)
        
        return result
        
        """ return a Value
            for (Expression expression : childrenList) {
            Value value = expression.evaluate();
            value.attach();
            values.add(value);
        }

        ExecutorFactory executorFactory = ExecutorFactory.getInstance();
        Value result = executorFactory.execute(this,values);
        
        for (Value value : values) {
            value.detach();
        }
        
        return result;
        """
    
    def get_name(self):
        raise Exception("Error. need to be redefined in children")
    
    def get_priority(self):
        raise Exception("Error. need to be redefined in children")
    
    def get_label(self):
        raise Exception("Error. need to be redefined in children")


class BinOpExpression(Expression):
    """ BinOpExpression
    """
    # Class members
    c_log = logging.getLogger("query.BinOpExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(BinOpExpression,self).__init__()
    
    def operator(self):
        raise Exception("Error. Need to be defined in children")
    
    def get_left(self):
        return self._children[0]
        
    def get_right(self):
        return self._children[1]
    
    def __repr__(self):
        
        left  = self.get_left()
        right = self.get_right()

        l = "( %s )"%(left) if left.get_priority < self.get_priority() else "%s"%(left)
        r = "( %s )"%(left) if right.get_priority < self.get_priority() else "%s"%(right)
        
        return "%s %s %s"%(l,self.operator(),r)

    def get_name(self):
        return "%number"
    

    def compute(self,a,b):
        raise Exception("Error. need to be redefined in children")
    
class Add(Expression):
    """ Add
    """
    # Class members
    c_log = logging.getLogger("query.Add")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(Add,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "+"
    
    def compute(self,a,b):
        return a+b
        
    def get_priority(self):
        return Expression.c_priority["sum"]

class Sub(Expression):
    """ Sub
    """
    # Class members
    c_log = logging.getLogger("query.Sub")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(Sub,self).__init__()
    
    def operator(self):
        return "-"
    
    def compute(self,a,b):
        return a-b
        
    def get_priority(self):
        return Expression.c_priority["sum"]

class Mul(Expression):
    """ Mul
    """
    # Class members
    c_log = logging.getLogger("query.Mul")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(Mul,self).__init__()
    
    def operator(self):
        return "*"
    
    def compute(self,a,b):
        return a*b
        
    def get_priority(self):
        return Expression.c_priority["prod"]

class Div(Expression):
    """ Div
    """
    # Class members
    c_log = logging.getLogger("query.Div")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(Div,self).__init__()
    
    def operator(self):
        return "/"
    
    def compute(self,a,b):
        return a/b
        
    def get_priority(self):
        return Expression.c_priority["prod"]
        
class NumberExpression(Expression):
    """ NumberExpression
    """
    
    # Class members
    c_log = logging.getLogger("query.NumberExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,val):
        """ constructor """
        
        super(NumberExpression,self).__init__()
        
        self._value = val
        
    def __repr__(self):
        
        return "%s"%(self._value)

    def get_value(self):
        return self._value

    def get_name(self):
        return "%number"
    
    def get_label(self):
        return self.__repr__()
    
    def get_priority(self):
        return Expression.c_priority["atom"]

class NameExpression(Expression):
    """ NameExpression
    """
    
    # Class members
    c_log = logging.getLogger("query.NameExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,val):
        """ constructor """
        
        super(NameExpression,self).__init__()
        
        self._value = val
        
    def __repr__(self):
        
        return "%s"%(self._value)

    def get_value(self):
        return self._value

    def get_name(self):
        return "%name"
    
    def get_label(self):
        return self.__repr__()

    def get_variable(self):
        return self._value
    
    def get_priority(self):
        return Expression.c_priority["atom"]

class StringExpression(Expression):
    """ StringExpression
    """
    
    # Class members
    c_log = logging.getLogger("query.StringExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,val):
        """ constructor """
        
        super(StringExpression,self).__init__()
        
        self._value = val
        
    def __repr__(self):
        
        return "%s"%(self._value)

    def get_value(self):
        return self._value

    def get_name(self):
        return "%string"
    
    def get_label(self):
        return self.__repr__()

    def get_variable(self):
        return self._value
    
    def get_priority(self):
        return Expression.c_priority["atom"]
    
class OperationFactory(object):
    
    c_log = logging.getLogger("query.OperationFactory")
    c_log.setLevel(logging.DEBUG)
    
    c_binary_operations = {
                        "<":"LT",
                        ">":"GT",
                        "+":Add,
                        "-":Sub,
                        "*":Mul,
                        "/":Div,
                        ">=":"GE",
                        "<=":"LE",
                        "<>":"NE",
                        "=":"EQ",
                        "**":"Pow",
                        "^":"Pow",
                        "&":"Merge",
                        "&&":"And",
                        "and":"And",
                        "||":"Or",
                        "or":"Or"
                       }
    
    c_unary_operations  = {
                         "-":"Neg",
                         "!":"Not" 
                       }
         
    def __init__(self):
        """ constructor """
       
    @classmethod
    def get_binary_operation(cls,bin_op): 
         
        # get classname from the c_binary_operation
        classname = OperationFactory.c_binary_operations.get(bin_op,None)
        
        if classname == None:
            raise Exception("Error %s is not a binary operation"%(bin_op))
        
        # create the binop
        # create object and update its internal dictionary
        inst = object.__new__(classname)
        
        inst.__dict__.update({'_children':[]})
        
        return inst
    

class ExpressionCompiler(object):
    """ create tokens for parsing the grammar. 
        This class is a wrapper around the python tokenizer adapt to the DSL that is going to be used.
    """
    
    # Class members
    c_log = logging.getLogger("query.ExpressionCompiler")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        
        self._tokenizer = None

        # the current statement used to create a pseudo iterator
        self._current_statement = None
        
        self._operator_types = OperatorTypes()

    def _read_expression(self):
        # read an expression
        return self._read_disjunction()
        
    def _read_disjunction(self):
        
        p = self._read_conjunction()
        
        while self._operator_types.is_disjunction(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_conjunction())
            p = op
        
        return p
            
        
    def _read_conjunction(self):
        
        p = self._read_test()
        
        while self._operator_types.is_conjunction(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_test())
            p = op
        
        return p
    
    def _read_test(self):
        """ read test """
        p = self._read_term()
        
        while self._operator_types.is_comparative(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_term())
            p = op 
        
        return p
     
    def _read_term(self):
        """ read term """
        p = self._read_factor()
        
        while self._operator_types.is_additive(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_factor())
            p = op
        
        return p
    
    def _read_factor(self):
        """ read factor """
        p = self._read_power()
        
        while self._operator_types.is_multiplicative(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_power())
            p = op
        
        return p
    
    def _read_power(self):
        """ read power """
        p = self._read_atom()
        
        while self._operator_types.is_power(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self._tokenizer.current_token().value)
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_atom())
            p = op
        
        return p

    def _read_atom(self):
        """ read atom """
        p = None
        
        token = self._tokenizer.current_token()
        
        type = token.type
        
        if type == "NUMBER":
            n = float(token.value)
            p = NumberExpression(n)
            self._tokenizer.next()
        elif type == "NAME":
            p = NameExpression(token.value)
            self._tokenizer.next()
            # check next token and do something if necessary
        elif type == "STRING":
            p = StringExpression(token.value)
            self._tokenizer.next()
        elif type == "OP":
            print "should have been detected"
        else:
            raise Exception("Invalid Token %s"%(token))
        
        return p

    def compile(self,a_tokenizer=None):
        """ compile the passed program.
        
            Args:
               program: the program to parse
               
            Returns:
               return 
        
            Raises:
               exception 
        """ 
        
        self._tokenizer = a_tokenizer
        
        # read expression
        return self._read_expression()
       
# unit tests part
import unittest
class TestExprCompiler(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testExprCompiler(self):
        
        c = ExpressionCompiler()
        
        tokenizer = Tokenizer()
        tokenizer.tokenize("1+2")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        expr.evaluate() #IGNORE:E1103
        
        