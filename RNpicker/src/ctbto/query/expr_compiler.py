""" 
    Copyright 2008 CTBTO
    
    compile the statements
"""
import logging

class OperationFactory(object):
    
    c_log = logging.getLogger("query.OperationFactory")
    c_log.setLevel(logging.DEBUG)
    
    c_binary_operations = {
                        "<":"LT",
                        ">":"GT",
                        "+":"Add",
                        "-":"Sub",
                        "*":"Mul",
                        "/":"Div",
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
       
    
    def get_binary_operation(self,bin_op): 
        
        """if bin_op in c_binary_operations:
            # create the right binary operation (add,mul)
            # make a factory of operations => return an expression
            
    
    public static Expression getBinaryOperation(String str) {
        if (binaryOperations.containsKey(str)) {
            String className = rootPackage+".binop."+binaryOperations.get(str);
            try {
                Class<?> c = Class.forName(className);
                return (Expression)c.newInstance();
            }
            catch (ClassNotFoundException e) {
                throw new RuntimeException("Class '"+className+"' not found");
            }
            catch (Exception e) {
                throw new RuntimeException("Error instantiating class '"+className+"'");
            }
        }
        
        throw new RuntimeException("Could not find an implementation for the given " + 
                "input type '" + str + "'.");
    }"""
    
    return Expression()

class OperatorTypes(object):
    
    c_log = logging.getLogger("query.OperatorTypes")
    c_log.setLevel(logging.DEBUG)
    
    c_additive       = set(["+","-","&"])
    c_multiplicative = set("*","/")
    c_comparative    = set("<",">","=","<=",">=","<>")
    c_power          = set("^","**")
    c_or             = set("or","||")
    c_and            = set("and","&&")
    
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
        
        if where not in c_type.keys():
            return False
        
        for s in c_type[where]:
            if what == s:
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
    
class Expression(object):
    """ the expression object => heart of the system
    """
    
    # Class members
    c_log = logging.getLogger("query.Expression")
    c_log.setLevel(logging.DEBUG)
    
    c_priority = {"or":1,"and":2,"test":3,"sum":4,"prod":5,"power":6,"unop":7,"atom":8}
    
    def __init__(self):
        """ constructor """
        
        # list of children
        self._children = []
        
    
    def add(self,child):
        """ add child in the expression """
        self._children.append(child)
    
    def evaluate(self):
        """ evaluate the expr => execute it """
        
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
        print "evaluate"
    
    def get_name(self):
        raise Exception("Error. need to be redefined in children")
    
    def get_priority(self):
        raise Exception("Error. need to be redefined in children")

class NumberExpression(object):
    """ NumberExpression
    """
    
    # Class members
    c_log = logging.getLogger("query.NumberExpression")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ constructor """
    

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
        self._read_disjunction()
        
    def _read_disjunction(self):
        
        p = self._read_conjunction()
        
        while self._operator_types.is_disjunction(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_conjunction())
            p = op;
        
        return p;
            
        
    def _read_conjunction(self):
        print "do something" 
        
        p = self._read_test()
        
        while self._operator_types.is_conjunction(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_test())
            p = op; 
        
        return p
    
    def _read_test(self):
        """ read test """
        p = read_term()
        
        while self._operator_types.is_comparative(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_term())
            p = op; 
        
        return p
     
    def _read_term(self):
        """ read term """
        p = read_factor()
        
        while self._operator_types.is_additive(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_factor())
            p = op; 
        
        return p
    
    def _read_factor(self):
        """ read factor """
        p = read_power()
        
        while self._operator_types.is_multiplicative(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_power())
            p = op; 
        
        return p
    
    def _read_power(self):
        """ read power """
        p = read_atom()
        
        while self._operator_types.is_power(self._tokenizer.current_token()):
            op = OperationFactory.get_binary_operation(self, self._tokenizer.current_token())
            op.add(p)
            self._tokenizer.next()
            op.add(self._read_atom())
            p = op; 
        
            return p

    def _read_atom(self):
        """ read atom """
        p = None
        
        token = self._tokenizer.current_token()
        
        type = token.type
        
        if type == "NUMBER":
            # create number expression
            print "numb expre"
        elif type == "NAME":
            print "ident expression"
        elif type == "STRING":
            print "String expression"
        elif type == "OP":
            print "should have been detected"
    
    """

    private Expression readAtom() {
        Expression p = null;
        String token = tokenizer.currentToken();
        int type = tokenizer.currentTokenType();

        switch (type) {

        case Tokenizer.NUMBER:
            double n = Double.parseDouble(token);
            p = new NumberExpression(n);
            tokenizer.advance();
            break;

        case Tokenizer.IDENTIFIER:
            p = new IdentExpression(token);
            tokenizer.advance();
            if (tokenizer.currentToken().equals("(")) {
                tokenizer.advance();
                p = FunctionFactory.getInstance().create(token);
                boolean isHash = readList(p,")");
                if (isHash)
                    ((Function) p).argumentIsHash();
                tokenizer.consumeToken(")");
            }
            else if (tokenizer.currentToken().equals("[")) {
                tokenizer.advance();
                p = new IndexExpression(p);
                @SuppressWarnings("unused")
                boolean isHash = readList(p,"]");
                tokenizer.consumeToken("]");
            }
            break;

        case Tokenizer.STRING:
            p = new StringExpression(token);
            tokenizer.advance();
            break;
            
        case Tokenizer.DATE:
            p = new DateExpression(token);
            tokenizer.advance();
            break;

        case Tokenizer.PUNCTUATION:

            switch (token.charAt(0)) {

            case '(':
                tokenizer.advance();
                p = readExpression();
                tokenizer.consumeToken(")");
                break;

            case '[':
                tokenizer.advance();
                p = new ListExpression();
                readList(p,"]");
                tokenizer.consumeToken("]");
                break;
                
            case '{':
                tokenizer.advance();
                p = new HashExpression();
                readList(p,"}");
                tokenizer.consumeToken("}");
                break;

            case '-':
                tokenizer.advance();
                p = new Neg(readAtom());
                break;

            case '!':
                tokenizer.advance();
                p = new Not(readAtom());
                break;
                
            case 'n': /* not */
                tokenizer.advance();
                p = new Not(readAtom());
                break;

            default:
                throw new RuntimeException("Invalid token [" + token + "]");
            }
            break;

        default:
            throw new RuntimeException("Invalid token [" + token + "," + type
                    + "]");
        }
        return p;
    }"""

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
        self._read_expression()
              
        