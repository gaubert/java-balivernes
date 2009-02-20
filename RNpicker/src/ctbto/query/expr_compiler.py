""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging
from tokenizer import Tokenizer

import ctbto.common.utils

class OperatorTypes(object):
    
    c_log = logging.getLogger("query.OperatorTypes")
    c_log.setLevel(logging.DEBUG)
    
    c_additive       = set(["+","-","&"])
    c_multiplicative = set(["*","/"])
    c_comparative    = set(["<",">","=","<=",">=","<>"])
    c_power          = set(["^","**"])
    c_or             = set(["or","||"])
    c_and            = set(["and","&&",","])
    
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

class NumberUnopExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.NumberUnopExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(NumberUnopExecutor,self).__init__(op)
     
    def execute(self,values):  
        
        # more or less than 1 elements => error
        if len(values) != 1:
            raise Exception("Error. A UnOp Operation has one and only one argument. Passed values = %s\n"%(values))
        
        return self._op.compute(values[0])  

class NumberExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.NumberExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(NumberExecutor,self).__init__(op)
        
        self._value = op.get_value()
     
    def execute(self,values): #IGNORE:W0613
        return self._value

class StringExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.StringExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(StringExecutor,self).__init__(op)
        
        self._value = op.get_value() 
     
    def execute(self,values):  #IGNORE:W0613
        return self._value

class NameExecutor(Executor):
    
     # Class members
    c_log = logging.getLogger("query.NameExecutor")
    c_log.setLevel(logging.DEBUG)
     
    def __init__(self,op):
        """ constructor """
        super(NameExecutor,self).__init__(op)
        
        self._value = op.get_value() 
     
    def execute(self,values):  #IGNORE:W0613
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
                              "%number:none"          :"NumberExecutor",
                              "%number:number"        :"NumberUnopExecutor",
                              "%string:none"          :"StringExecutor",
                              "%number:number:number" :"NumberBinopExecutor",
                              "%name:none"            :"NameExecutor",
                              "%cos:number"           :"CosExecutor",
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
        
        print("sig:[%s]\n"%(signature))
        
        classname = Expression.c_executor_dispatcher.get(signature,None)
        
        if classname == None:
            raise Exception("Error cannot find the right dispatch for %s"%(signature))
        
        executor = ctbto.common.utils.new_instance("ctbto.query.expr_compiler", classname,expr)
        
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
    
    def get_execution_tree(self):
        """ return the expression representation """
        return self.__repr__()
    
    def __repr__(self):
        
        """ evaluate the expr => execute it """
        s = ""
        
        # for each child in the children list
        for expr in self._children:
            v = expr.__repr__()
            s += "%s "%(v)
        
        return s
    
    def get_name(self):
        raise Exception("Error. need to be redefined in children")
    
    def get_priority(self):
        raise Exception("Error. need to be redefined in children")
    
    def get_label(self):
        raise Exception("Error. need to be redefined in children")

class UnOpExpression(Expression):
    """ UnaryExpression
    """
    # Class members
    c_log = logging.getLogger("query.UnOpExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(UnOpExpression,self).__init__()
    
    def operator(self):
        raise Exception("Error. Need to be defined in children")
    
    def compute(self,value):
        raise Exception("Error. Need to be defined in children")
    
    def get_name(self):
        # return classname
        raise Exception("Error. need to be redefined in children")
    
    def _getChild(self):
        return self._children[0]
    
    def get_priority(self):
        return Expression.c_priority["unop"]
    
    def __repr__(self):
        
        expr = self._getChild()
        
        l =  "( %s )"%(kid) if expr.priority() <= self.get_priority() else "%s"%(kid)
        
        return l

class NotExpression(UnOpExpression):
    """ NotExpression
    """
    # Class members
    c_log = logging.getLogger("query.NotExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,expr):
        """ constructor """
        super(NotExpression,self).__init__()
        self.add(expr)
    
    def compute(self,value):
        return (1 if value == 0 else 0)
    
    def operator(self):
        return "not"
    
    def get_name(self):
        return "%number"
    
    def __repr__(self):
        return "(not %s)"%(super(NotExpression,self).__repr__())
    
class NegExpression(UnOpExpression):
    """ NegExpression
    """
    # Class members
    c_log = logging.getLogger("query.NegExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,expr):
        """ constructor """
        super(NegExpression,self).__init__()
        self.add(expr)
    
    def compute(self,value):
        return -value
    
    def operator(self):
        return "-"
    
    def get_name(self):
        return "%number"
    
    def __repr__(self):
        return "( - %s)"%(super(NegExpression,self).__repr__())

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
    
    def print_expression(self):
        
        left  = self.get_left()
        right = self.get_right()

        l = "( %s )"%(left) if left.get_priority < self.get_priority() else "%s"%(left)
        r = "( %s )"%(left) if right.get_priority < self.get_priority() else "%s"%(right)
        
        return "%s %s %s"%(l,self.operator(),r)

    def get_name(self):
        return "%number"
    
    def compute(self,a,b):
        raise Exception("Error. need to be redefined in children")
    
class GTExpression(Expression):
    """ Greater than
    """
    # Class members
    c_log = logging.getLogger("query.GTExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(GTExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return ">"
    
    def compute(self,a,b):
        return (1 if a>b else 0)
    
    def __repr__(self):
        return "( > %s)"%(super(GTExpression,self).__repr__())
        
    def get_priority(self):
        return Expression.c_priority["test"]

class LTExpression(Expression):
    """ Lower than
    """
    # Class members
    c_log = logging.getLogger("query.LTExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(LTExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "<"
    
    def __repr__(self):
        return "( < %s)"%(super(LTExpression,self).__repr__())
    
    def compute(self,a,b):
        return (1 if a<b else 0)
        
    def get_priority(self):
        return Expression.c_priority["test"]

class LEExpression(Expression):
    """ Lower Equal than
    """
    # Class members
    c_log = logging.getLogger("query.LEExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(LEExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "<="
    
    def __repr__(self):
        return "( <= %s)"%(super(LEExpression,self).__repr__())
    
    def compute(self,a,b):
        return (1 if a<=b else 0)
        
    def get_priority(self):
        return Expression.c_priority["test"]

class GEExpression(Expression):
    """ Greater Equal than
    """
    # Class members
    c_log = logging.getLogger("query.GEExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(GEExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return ">="
    
    def compute(self,a,b):
        return (1 if a>=b else 0)
        
    def get_priority(self):
        return Expression.c_priority["test"]
    
    def __repr__(self):
        return "( >= %s)"%(super(GEExpression,self).__repr__())

class EQExpression(Expression):
    """ Equal than
    """
    # Class members
    c_log = logging.getLogger("query.EQExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(EQExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "="
    
    def compute(self,a,b):
        return (1 if a == b else 0)
        
    def get_priority(self):
        return Expression.c_priority["test"]
    
    def __repr__(self):
        s = super(EQExpression,self).__repr__()
        return "( = %s)"%(s)
        

class NEExpression(Expression):
    """ Non Equal than
    """
    # Class members
    c_log = logging.getLogger("query.NEExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(NEExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "<>"
    
    def __repr__(self):
        return "( <> %s)"%(super(NEExpression,self).__repr__())
    
    def compute(self,a,b):
        return (1 if a != b else 0)
        
    def get_priority(self):
        return Expression.c_priority["test"]
    
class AddExpression(BinOpExpression):
    """ Add
    """
    # Class members
    c_log = logging.getLogger("query.AddExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(AddExpression,self).__init__()
    
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "+"
    
    def __repr__(self):
        return "( + %s)"%(super(AddExpression,self).__repr__())
    
    def compute(self,a,b):
        return a+b
        
    def get_priority(self):
        return Expression.c_priority["sum"]

class SubExpression(BinOpExpression):
    """ Sub
    """
    # Class members
    c_log = logging.getLogger("query.SubExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(SubExpression,self).__init__()
        
    def get_name(self):
        return "%number"
    
    def operator(self):
        return "-"
    
    def __repr__(self):
        return "( - %s)"%(super(SubExpression,self).__repr__())
    
    def compute(self,a,b):
        return a-b
        
    def get_priority(self):
        return Expression.c_priority["sum"]

class MulExpression(BinOpExpression):
    """ Mul
    """
    # Class members
    c_log = logging.getLogger("query.MulExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(MulExpression,self).__init__()
    
    def operator(self):
        return "*"
    
    def __repr__(self):
        return "( * %s)"%(super(MulExpression,self).__repr__())
    
    def get_name(self):
        return "%number"
    
    def compute(self,a,b):
        return a*b
        
    def get_priority(self):
        return Expression.c_priority["prod"]

class AndExpression(BinOpExpression):
    """ And
    """
    # Class members
    c_log = logging.getLogger("query.AndExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(AndExpression,self).__init__()
    
    def operator(self):
        return "and"
    
    def __repr__(self):
        return "( and %s)"%(super(AndExpression,self).__repr__())
    
    def compute(self,a,b):
        return (a and b)
        
    def get_priority(self):
        return Expression.c_priority["and"]

class OrExpression(BinOpExpression):
    """ OrExpression
    """
    # Class members
    c_log = logging.getLogger("query.OrExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(OrExpression,self).__init__()
    
    def operator(self):
        return "or"
    
    def __repr__(self):
        return "( or %s)"%(super(OrExpression,self).__repr__())
    
    def compute(self,a,b):
        return (a or b)
        
    def get_priority(self):
        return Expression.c_priority["or"]

class DivExpression(Expression):
    """ Div
    """
    # Class members
    c_log = logging.getLogger("query.DivExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
        super(DivExpression,self).__init__()
    
    def operator(self):
        return "/"
    
    def __repr__(self):
        return "( / %s)"%(super(DivExpression,self).__repr__())
    
    def compute(self,a,b):
        return a/b
    
    def get_name(self):
        return "%number"
        
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
        
        return "( literal %s )"%(self._value)

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
        
        return "( literal %s )"%(self._value)

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

class ItemAssignementExpression(Expression):
    """ 
        ItemAssignementExpression
    """
    
    # Class members
    c_log = logging.getLogger("query.ItemAssignementExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,a_variable,a_index):
        """ constructor """
        
        super(ItemAssignementExpression,self).__init__()
        
        self._variable = a_variable
        self._index    = a_index
        
    def __repr__(self):
        
        return "( item_assign %s ( index %s ) )"%(self._variable,self._index)

    def get_name(self):
        return "%item_assignment"
    
    def get_label(self):
        return self.__repr__()

    def get_variable(self):
        return self._variable
    
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
        
        return "( literal %s )"%(self._value)

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
                        "<"  :"LTExpression",
                        ">"  :"GTExpression",
                        "+"  :"AddExpression",
                        "-"  :"SubExpression",
                        "*"  :"MulExpression",
                        "/"  :"DivExpression",
                        ">=" :"GEExpression",
                        "<=" :"LEExpression",
                        "<>" :"NEExpression",
                        "="  :"EQExpression",
                        "**" :"PowExpression",
                        "^"  :"PowExpression",
                        "&"  :"MergeExpression",
                        "&&" :"AndExpression",
                        ","  :"AndExpression",
                        "and":"AndExpression",
                        "||" :"OrExpression",
                        "or" :"OrExpression"
                       }
    
    c_unary_operations  = {
                         "-":"NegExpression",
                         "!":"NotExpression" 
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
        inst = ctbto.common.utils.new_instance("ctbto.query.expr_compiler",classname)
        
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

    def read_expression(self):
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

    def _read_item_assignment(self):
        """ read an item assignment expression """
        
        var = p = NameExpression(self._tokenizer.current_token().value)
        
        self._tokenizer.next()
        
        self._tokenizer.consume_token('[')
        
        index = self.read_expression()
        
        self._tokenizer.consume_token(']')
        
        return ItemAssignementExpression(var,index)
        
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
            if token.value == 'not':
                self._tokenizer.next()
                p = NotExpression(self._read_atom())
            elif self._tokenizer.advance().value == '[':
                p = self._read_item_assignment()
            else:
                p = NameExpression(token.value)
                self._tokenizer.next()
        elif type == "STRING":
            p = StringExpression(token.value)
            self._tokenizer.next()
        elif type == "OP":
            if token.value == '(':
                self._tokenizer.next()
                p = self.read_expression()
                self._tokenizer.consume_token(')')
            elif token.value == '-':
                self._tokenizer.next()
                p = NegExpression(self._read_atom())
            else:
                raise Exception("Invalid Operator Token %s"%(token))
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
        return self.read_expression()
       
# unit tests part
import unittest
class TestExprCompiler(unittest.TestCase):
    
    def setUp(self):
         
        print " setup \n"
    
    def testEvaluateBooleanExpression(self):
        
        c = ExpressionCompiler()
        
        tokenizer = Tokenizer()
        tokenizer.tokenize("3 < 2")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("1 < 2")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("3 <= 2")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("3 <= 10")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("100 <= 100")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("10 > 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("1000 > 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("10 >= 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("1000 >= 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("1000 >= 1000")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("1000 = 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("20 = 20")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("20 <> 21")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
        tokenizer.tokenize("21 <> 21")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0,result)
        
        tokenizer.tokenize("not(21 <> 21)")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(1,result)
        
    def testEvaluateAdditivity(self):
        
        c = ExpressionCompiler()
        
        tokenizer = Tokenizer()
        tokenizer.tokenize("1+2")
        tokenizer.next()
        
        expr = c.compile(tokenizer)       
        
        result = expr.evaluate() #IGNORE:E1103
        
        print("result = %s\n"%(result))
        
        self.assertEqual(3.0,result)
        
        print("Test multiple additions \n")
        
        tokenizer.tokenize("1+2+3+4")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print("result = %s\n"%(result))
        
        self.assertEqual(10.0,result)
        
        print("Test multiple substractions \n")
        
        tokenizer.tokenize("1-3+4+5")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print("result = %s\n"%(result))
        
        self.assertEqual(7.0,result)
        
        tokenizer.tokenize("1-7-3+4+5")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print("result = %s\n"%(result))
        
        self.assertEqual(0.0,result)
        
        tokenizer.tokenize("7-7+17-18")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print("result = %s\n"%(result))
        
        self.assertEqual(-1.0,result)
        
        tokenizer.tokenize("-7-7+17-4")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print("result = %s\n"%(result))
        
        self.assertEqual(-1.0,result)
        
    def testEvaluateNegation(self):
         
        c = ExpressionCompiler()
        tokenizer = Tokenizer()
        
        tokenizer.tokenize("not 0")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print "result = %s\n"%(result)
        
        self.assertEqual(1,result)
        
    
    def testEvaluateFactors(self):
        
        c = ExpressionCompiler()
        
        tokenizer = Tokenizer()
        tokenizer.tokenize("7*7")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print "result = %s\n"%(result)
        
        self.assertEqual(49.0,result)
        
        tokenizer.tokenize("7*7/7")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        result = expr.evaluate()
        
        print "result = %s\n"%(result)
        
        self.assertEqual(7.0,result)
        
    def testExecutionTreeWithTerms(self):
        
        c = ExpressionCompiler()
        tokenizer = Tokenizer()
        
        tokenizer.tokenize("A=1")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        self.assertEqual("( = ( literal A ) ( literal 1.0 ) )",expr.get_execution_tree())
        
        tokenizer.tokenize("A=1 and B>10")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        print "Execution Tree = %s\n"%(expr.get_execution_tree())
        
        self.assertEqual("( and ( = ( literal A ) ( literal 1.0 ) ) ( > ( literal B ) ( literal 10.0 ) ) )",expr.get_execution_tree())
        
        tokenizer.tokenize("(A=1 and B>10) or (C > 10)")
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        print "Execution Tree = %s\n"%(expr.get_execution_tree())
        
    
    def testExecutionTreeWithItemAssignment(self):
        
        c = ExpressionCompiler()
        tokenizer = Tokenizer()
        
        tokenizer.tokenize("A[B]= 1 + R")
        
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        exec_tree = expr.get_execution_tree()
        
        print "Expression Tree %s\n"%(exec_tree)
        
        self.assertEqual("( = ( item_assign ( literal A ) ( index ( literal B ) ) ) ( + ( literal 1.0 ) ( literal R ) ) )",exec_tree)
        
        # a little bit more complex
        tokenizer.tokenize("A[B+(C*3)+1]= 1 + R")
        
        tokenizer.next()
        
        expr = c.compile(tokenizer)
        
        exec_tree = expr.get_execution_tree()
        
        print "Expression Tree %s\n"%(exec_tree)
        
        self.assertEqual("( = ( item_assign ( literal A ) ( index ( + ( + ( literal B ) ( * ( literal C ) ( literal 3.0 ) ) ) ( literal 1.0 ) ) ) ) ( + ( literal 1.0 ) ( literal R ) ) )",exec_tree)
        
        
        
        
        
        
        
        
        
        