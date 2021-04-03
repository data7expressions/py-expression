import re
import math
from enum import Enum

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ExpressionError(Exception):pass

class Operand():
    @property
    def value(self): 
        pass

    def __add__(self, other):return Addition([other,self]) 
    def __sub__(self, other):return Subtraction([other,self])    
    def __mul__(self, other):return Multiplication([other,self])
    # def __pow__(self, other):return Exponentiation([other,self]) 
    def __truediv__(self, other):return Division([other,self]) 
    # def __floordiv__(self, other):return FloorDivision([other,self]) 
    def __mod__(self, other):return Mod([other,self])

    def __lshift__(self, other):return LeftShift([other,self])
    def __rshift__(self, other):return RightShift([other,self])
    def __and__(self, other):return BitAnd([other,self])
    def __or__(self, other):return BitOr([other,self])
    def __xor__(self, other):return BitXor([other,self])
    def __invert__(self, other):return BitNot([other,self])

    def __lt__(self, other):return LessThan([other,self])
    def __le__(self, other):return LessThanOrEqual([other,self])
    def __eq__(self, other):return Equal([other,self])
    def __ne__(self, other):return NotEqual([other,self])
    def __gt__(self, other):return GreaterThan([other,self])
    def __ge__(self, other):return GreaterThanOrEqual([other,self])

    def __not__(self):return Not([self])
    def __and2__(self, other):return And([other,self])
    def __or2__(self, other):return Or([other,self])

    def __isub__(self, other):return AssigmentSubtraction([other,self])
    def __iadd__(self, other):return AssigmentAddition([other,self])
    def __imul__(self, other):return AssigmentMultiplication([other,self])
    def __idiv__(self, other):return AssigmentDivision([other,self])
    def __ifloordiv__(self, other):return AssigmentFloorDivision([other,self])
    def __imod__(self, other):return AssigmentMod([other,self])
    def __ipow__(self, other):return AssigmentExponentiation([other,self])

    def eval(self,context:dict=None):
        parser = Parser()
        if context != None:
            parser.setContext(self,context)
        return self.value

    def vars(self):
        parser = Parser()
        return parser.getVars(self)
    def constants(self):
        parser = Parser()
        return parser.getConstants(self) 
    def operators(self):
        parser = Parser()
        return parser.getOperators(self)
    def functions(self):
        parser = Parser()
        return parser.getFunctions(self)

         
        

class Constant(Operand):
    def __init__(self,value,type ):
      self._value  = value
      self._type  = type

    @property
    def value(self): 
        return self._value
    @property
    def type(self): 
        return self._type     

    def __str__(self):
        return str(self._value)
    def __repr__(self):
        return str(self._value)  
class Variable(Operand):
    def __init__(self,name ):
      self._name  = name
      self._names = name.split('.')
      self._context  = None

    @property
    def name(self):
        return self._name

    @property
    def context(self):
        return self._context
    @context.setter
    def context(self,value):
        self._context=value

    @property
    def value(self):
        _value = self._context
        for n in self._names:
            _value=_value[n]
        return _value

    @value.setter
    def value(self,value):
        _value = self._context
        length = len(self._names)
        i=1
        for n in self._names:
            if i == length:
                _value[n]=value
            else:                    
                _value=_value[n]
            i+=1

    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name      
class KeyValue(Operand):
    def __init__(self,name,value:Operand):
      super(KeyValue,self).__init__([value])
      self._name  = name

    @property
    def name(self):
        return self._name  
    @property
    def value(self): 
        return self._operands[0].value

class Operation(Operand):
    def __init__(self,operands ):
      self._operands  = operands   

    @property
    def operands(self):
        return self._operands

    @property
    def value(self):
        pass
class Function(Operation):
    def __init__(self,mgr,name,args,isChild=False):
      super(Function,self).__init__(args)
      self.mgr  = mgr
      self.name  = name
      self._isChild  = isChild

    @property
    def isChild(self):
        return self._isChild
    @isChild.setter
    def isChild(self,value):
        self._isChild=value
    @property
    def value(self): 
        args=[]
        if self._isChild:
            parent = self._operands.pop(0)
            value = parent.value
            _type = type(value).__name__
            function=self.mgr.getFunction(self.name,_type)            
            for p in self._operands:args.append(p.value)
            args.insert(0,value)            
        else:
            function=self.mgr.getFunction(self.name)
            for p in self._operands:args.append(p.value)    

        return function(*args)
class Array(Operation):
    def __init__(self,elements=[]):
      super(Array,self).__init__([elements])

    @property
    def value(self):
        list= []
        for p in self._operands:
            list.append(p.value)
        return list 
class Object(Operation):
    def __init__(self,attributes=[]):
      super(Object,self).__init__(attributes)

    @property
    def value(self):
        dic= {}
        for p in self._operands:
            dic[p.name]=p.value
        return dic 
class Operator(Operation):
    def __init__(self,operands ):
      super(Operator,self).__init__(operands)
      self._name=""
      self._category=""

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name=value 
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self,value):
        self._category=value        

    @property
    def value(self):
        val=self._operands[0].value
        l=len(self._operands)
        i=1
        while i<l:
            val=self.solve(val,self._operands[i].value)
            i+=1
        return val  

    def solve(self,a,b):
        pass 

class NegativeDecorator(Operator):
    def __init__(self,operand:Operand ):
        super(NegativeDecorator,self).__init__([operand])

    @property
    def value(self): 
        return self._operands[0].value * -1
class NotDecorator(Operator):
    def __init__(self,operand:Operand ):
      super(NotDecorator,self).__init__([operand])

    @property
    def value(self): 
        return not self._operands[0].value 
class IndexDecorator(Operator):
    def __init__(self,operand:Operand,idx:Operand ):
      super(IndexDecorator,self).__init__([operand,idx])        

    @property
    def value(self): 
        return self._operands[0].value[self._operands[1].value]
class Addition(Operator):
    def solve(self,a,b):
        return a+b 
class Subtraction (Operator):
    def solve(self,a,b):
        return a-b   
class Multiplication(Operator):
    def solve(self,a,b):
        return a*b 
class Division (Operator):
    def solve(self,a,b):
        return a/b  
class Exponentiation(Operator):
    def solve(self,a,b):
        return a**b 
class FloorDivision (Operator):
    def solve(self,a,b):
        return a//b   
class Mod (Operator):
    def solve(self,a,b):
        return a%b 

class BitAnd(Operator):
    def solve(self,a,b):
        return a & b 
class BitOr(Operator):
    def solve(self,a,b):
        return a | b
class BitXor(Operator):
    def solve(self,a,b):
        return a ^ b                  
class BitNot(Operator):
    @property
    def value(self):
        return ~ self._operands[0].value
class LeftShift(Operator):
    def solve(self,a,b):
        return a << b   
class RightShift(Operator):
    def solve(self,a,b):
        return a >> b   

class Equal(Operator):
    def solve(self,a,b):
        return a==b
class NotEqual(Operator):
    def solve(self,a,b):
        return a!=b          
class GreaterThan(Operator):
    def solve(self,a,b):
        return a>b
class LessThan(Operator):
    def solve(self,a,b):
        return a<b 
class GreaterThanOrEqual(Operator):
    def solve(self,a,b):
        return a>=b
class LessThanOrEqual(Operator):
    def solve(self,a,b):
        return a<=b                

class And(Operator):
    @property
    def value(self):
        if not self._operands[0].value : return False
        return self._operands[1].value
class Or(Operator):
    @property
    def value(self):
        if self._operands[0].value : return True
        return self._operands[1].value
class Not(Operator):
    @property
    def value(self):
        return not self._operands[0].value

class Assigment(Operator):
    @property
    def value(self):
        self._operands[0].value = self._operands[1].value
        return self._operands[0].value
class AssigmentAddition(Operator):
    @property
    def value(self):
        self._operands[0].value += self._operands[1].value
        return self._operands[0].value
class AssigmentSubtraction (Operator):
    @property
    def value(self):
        self._operands[0].value -= self._operands[1].value
        return self._operands[0].value  
class AssigmentMultiplication(Operator):
    @property
    def value(self):
        self._operands[0].value *= self._operands[1].value
        return self._operands[0].value 
class AssigmentDivision (Operator):
    @property
    def value(self):
        self._operands[0].value /= self._operands[1].value
        return self._operands[0].value  
class AssigmentExponentiation(Operator):
    @property
    def value(self):
        self._operands[0].value **= self._operands[1].value
        return self._operands[0].value 
class AssigmentFloorDivision (Operator):
    @property
    def value(self):
        self._operands[0].value //= self._operands[1].value
        return self._operands[0].value   
class AssigmentMod (Operator):
    @property
    def value(self):
        self._operands[0].value %= self._operands[1].value
        return self._operands[0].value 
class AssigmentBitAnd(Operator):
    @property
    def value(self):
        self._operands[0].value &= self._operands[1].value
        return self._operands[0].value 
class AssigmentBitOr(Operator):
    @property
    def value(self):
        self._operands[0].value |= self._operands[1].value
        return self._operands[0].value
class AssigmentBitXor(Operator):
    @property
    def value(self):
        self._operands[0].value ^= self._operands[1].value
        return self._operands[0].value
class AssigmentLeftShift(Operator):
    @property
    def value(self):
        self._operands[0].value <<= self._operands[1].value
        return self._operands[0].value
class AssigmentRightShift(Operator):
    @property
    def value(self):
        self._operands[0].value >>= self._operands[1].value
        return self._operands[0].value

class Parser(metaclass=Singleton):
    def __init__(self):
       self._operators={}
       self._tripleOperators = []
       self._doubleOperators = [] 
       self._enums={} 
       self._functions={}
       self.initOperators()
       self.generalFunctions()
       self.mathFunctions()
       self.stringFunctions()
       self.initEnums()
       self.refresh()
             

    def initOperators(self):       

        self.addOperator('+','arithmetic',Addition,4)
        self.addOperator('-','arithmetic',Subtraction,4)
        self.addOperator('*','arithmetic',Multiplication,5)
        self.addOperator('/','arithmetic',Division,5)
        self.addOperator('**','arithmetic',Exponentiation,6)
        self.addOperator('//','arithmetic',FloorDivision,6)
        self.addOperator('%','arithmetic',Mod,7)

        self.addOperator('&','bitwise',BitAnd)
        self.addOperator('|','bitwise',BitOr)
        self.addOperator('^','bitwise',BitXor)
        self.addOperator('~','bitwise',BitNot)
        self.addOperator('<<','bitwise',LeftShift)
        self.addOperator('>>','bitwise',RightShift)

        self.addOperator('==','comparison',Equal,3)
        self.addOperator('!=','comparison',NotEqual,3)
        self.addOperator('>','comparison',GreaterThan,3)
        self.addOperator('<','comparison',LessThan,3)
        self.addOperator('>=','comparison',GreaterThanOrEqual,3)
        self.addOperator('<=','comparison',LessThanOrEqual,3)

        self.addOperator('&&','logical',And,2)
        self.addOperator('||','logical',Or,2)
        self.addOperator('!','logical',Not)

        self.addOperator('=','assignment',Assigment,1)
        self.addOperator('+=','assignment',AssigmentAddition,1)
        self.addOperator('-=','assignment',AssigmentSubtraction,1)
        self.addOperator('*=','assignment',AssigmentMultiplication,1)
        self.addOperator('/=','assignment',AssigmentDivision,1)
        self.addOperator('**=','assignment',AssigmentExponentiation,1)
        self.addOperator('//=','assignment',AssigmentFloorDivision,1)
        self.addOperator('%=','assignment',AssigmentMod,1)
        self.addOperator('&=','assignment',AssigmentBitAnd,1)
        self.addOperator('|=','assignment',AssigmentBitOr,1)
        self.addOperator('^=','assignment',AssigmentBitXor,1)
        self.addOperator('<<=','assignment',AssigmentLeftShift,1)
        self.addOperator('>>=','assignment',AssigmentRightShift,1)

    def generalFunctions(self): 
        self.addFunction('nvl',lambda a,b: a if a!=None else b )
    def mathFunctions(self):
        self.addFunction('ceil',math.ceil)
        self.addFunction('copysign',math.copysign) 
        self.addFunction('factorial',math.factorial) 
        self.addFunction('floor',math.floor) 
        self.addFunction('fmod',math.fmod) 
        self.addFunction('frexp',math.frexp) 
        self.addFunction('fsum',math.fsum) 
        self.addFunction('isfinite',math.isfinite) 
        self.addFunction('isnan',math.isnan) 
        self.addFunction('ldexp',math.ldexp) 
        self.addFunction('modf',math.modf) 
        self.addFunction('trunc',math.trunc) 
        self.addFunction('exp',math.exp) 
        self.addFunction('expm1',math.expm1) 
        self.addFunction('log',math.log) 
        self.addFunction('log1p',math.log1p) 
        self.addFunction('log2',math.log2) 
        self.addFunction('log10',math.log10) 
        self.addFunction('pow',math.pow) 
        self.addFunction('sqrt',math.sqrt) 
        self.addFunction('acos',math.acos) 
        self.addFunction('asin',math.asin) 
        self.addFunction('atan',math.atan) 
        self.addFunction('atan2',math.atan2) 
        self.addFunction('cos',math.cos) 
        self.addFunction('hypot',math.hypot) 
        self.addFunction('sin',math.sin) 
        self.addFunction('tan',math.tan) 
        self.addFunction('degrees',math.degrees)
        self.addFunction('radians',math.radians)
        self.addFunction('acosh',math.acosh)
        self.addFunction('asinh',math.asinh)
        self.addFunction('atanh',math.atanh)
        self.addFunction('cosh',math.cosh)
        self.addFunction('sinh',math.sinh)
        self.addFunction('tanh',math.tanh)
        self.addFunction('erf',math.erf)
        self.addFunction('erfc',math.erfc)
        self.addFunction('gamma',math.gamma)
        self.addFunction('lgamma',math.lgamma)
        self.addFunction('pi',math.pi)
        self.addFunction('e',math.e)
    def stringFunctions(self):
        # https://docs.python.org/2.5/lib/string-methods.html



        self.addFunction('capitalize',str.capitalize,['str'])
        self.addFunction('count',str.count,['str'])
        self.addFunction('encode',str.encode,['str'])
        self.addFunction('endswith',str.endswith,['str'])
        self.addFunction('find',str.find,['str'])
        self.addFunction('index',str.index,['str'])
        self.addFunction('isalnum',str.isalnum,['str'])
        self.addFunction('isalpha',str.isalpha,['str'])
        self.addFunction('isdigit',str.isdigit,['str'])
        self.addFunction('islower',str.islower,['str'])
        self.addFunction('isspace',str.isspace,['str'])
        self.addFunction('istitle',str.istitle,['str'])
        self.addFunction('isupper',str.isupper,['str'])
        self.addFunction('join',str.join,['str'])
        self.addFunction('ljust',str.ljust,['str'])
        self.addFunction('lower',str.lower,['str'])
        self.addFunction('lstrip',str.lstrip,['str'])
        self.addFunction('partition',str.partition,['str'])
        self.addFunction('replace',str.replace,['str'])
        self.addFunction('rfind',str.rfind,['str'])
        self.addFunction('rindex',str.rindex,['str'])
        self.addFunction('rjust',str.rjust,['str'])
        self.addFunction('rpartition',str.rpartition,['str'])
        self.addFunction('rsplit',str.rsplit,['str'])
        self.addFunction('rstrip',str.lstrip,['str'])
        self.addFunction('split',str.split,['str'])
        self.addFunction('splitlines',str.splitlines,['str'])
        self.addFunction('startswith',str.startswith,['str'])
        self.addFunction('strip',str.lstrip,['str'])
        self.addFunction('swapcase',str.swapcase,['str'])
        self.addFunction('title',str.title,['str'])
        self.addFunction('translate',str.translate,['str'])
        self.addFunction('upper',str.upper,['str'])
        self.addFunction('zfill',str.zfill,['str'])   
    def initEnums(self): 
        self.addEnum('DayOfWeek',{"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5,"Saturday":6,"Sunday":0})        
    
    def refresh(self):
        for key in self._operators.keys():
            if len(key)==2: self._doubleOperators.append(key)
            elif len(key)==3: self._tripleOperators.append(key)
    
    @property
    def doubleOperators(self):
        return self._doubleOperators

    @property
    def tripleOperators(self):
        return self._tripleOperators   

    def newOperator(self,key,operands):
        try: 
            operator = self._operators[key];               
            op= operator["imp"](operands)
            op.name = key
            op.category = operator["category"]
            return op
        except:
            raise ExpressionError('error with operator: '+str(key))  
    def priority(self,key):
        return self._operators[key]["priority"] if key in self._operators else -1          
    def addOperator(self,key:str,category:str,imp:Operator,priority:int=-1):        
        self._operators[key]={"category":category,"priority":priority,"imp":imp}
    def addEnum(self,key,source):
        if(type(source).__name__ == 'dict'):
            self._enums[key] =source
        elif issubclass(source, Enum):
            list ={}
            enum = {name: value for name, value in vars(source).items() if name.isupper()}
            for p in enum:
                list[p]=enum[p].value
            self._enums[key] =list
        else:
            raise ExpressionError('enum not supported: '+key)      
    def isEnum(self,name):    
        names = name.split('.')
        return names[0] in self._enums.keys()
    def getEnumValue(self,name,option): 
        return self._enums[name][option]
    def getEnum(self,name): 
        return self._enums[name]
    def addFunction(self,key,imp,types=['any']):
        if key not in self._functions.keys():
            self._functions[key]= []
        self._functions[key].append({'types':types,'imp':imp})         
    def getFunction(self,key,type='any'):
        for p in self._functions[key]:
            if type in p['types']:
                return p['imp']
        return None
    def solve(self,string:str,context:dict=None):        
        expression=self.parse(string)
        return expression.eval(context) 
    def parse(self,string)->Operand:
        try:            
            parser = _Parser(self,string)
            expression= parser.parse() 
            del parser
            return expression  
        except Exception as error:
            raise ExpressionError('expression: '+string+' error: '+str(error))

    def getVars(self,expression):
        list = {}
        if type(expression).__name__ ==  'Variable':
            list[expression.name] = "any"
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if type(p).__name__ ==  'Variable':
                    list[p.name] = "any"
                elif hasattr(p, 'operands'):
                    subList= self.getVars(p)
                    list = {**list, **subList}
        return list        
    def getConstants(self,expression):
        list = {}
        if type(expression).__name__ ==  'Constant':
            list[expression.value] = expression.type
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if type(p).__name__ ==  'Constant':
                    list[p.value] = p.type
                elif hasattr(p, 'operands'):
                    subList= self.getConstants(p)
                    list = {**list, **subList}
        return list
    def getOperators(self,expression):
        list = {}
        if isinstance(expression,Operator):
            list[expression.name] = expression.category
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if isinstance(p,Operator):
                    list[p.name] = p.category
                elif hasattr(p, 'operands'):
                    subList= self.getOperators(p)
                    list = {**list, **subList}
        return list
    def getFunctions(self,expression):
        list = {}
        if type(expression).__name__ ==  'Function':
            list[expression.name] = {"isChild":expression.isChild}
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if type(p).__name__ ==  'Function':
                    list[p.name] =  {"isChild":p.isChild}
                elif hasattr(p, 'operands'):
                    subList= self.getFunctions(p)
                    list = {**list, **subList}
        return list
        
    def setContext(self,expression,context):
        if type(expression).__name__ ==  'Variable':
            expression.context = context
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if type(p).__name__ ==  'Variable':
                    p.context = context
                elif hasattr(p, 'operands'):
                    self.setContext(p,context)           

class _Parser():
    def __init__(self,mgr,string):
       self.mgr = mgr 
       self.chars = self.clear(string)
       self.length=len(self.chars)
       self.index=0
       self.reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$') 
       self.reInt = re.compile('[0-9]+$')
       self.reFloat = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')
  

    @staticmethod
    def clear(string):
        isString=False
        quotes=None
        result =[]
        chars = list(string)
        for p in chars:
            if isString and p == quotes: isString=False 
            elif not isString and (p == '\'' or p=='"'):
                isString=True
                quotes=p
            if p != ' ' or isString:
               result.append(p)
        return result

    def parse(self):
        operands=[]
        while not self.end:
            operand =self.getExpression(_break=';')
            if operand is None:break
            operands.append(operand)
        if len(operands)==1 :
            return operands[0]
        return Array(operands) 

    @property
    def previous(self):
        return self.chars[self.index-1] 
    @property
    def current(self):
        return self.chars[self.index]    
    @property
    def next(self):
        return self.chars[self.index+1]
    @property
    def end(self):
        return self.index >= self.length   

    def getExpression(self,a=None,op1=None,_break=''):
        expression = None
        b = None
        isbreak = False               
        while not self.end:
            if a is None and op1 is None: 
                a=  self.getOperand()
                op1= self.getOperator()
                if op1 is None or op1 in _break: 
                    expression = a
                    isbreak= True
                    break
            b=  self.getOperand()
            op2= self.getOperator()
            if op2 is None or op2 in _break:
                expression= self.mgr.newOperator(op1,[a,b])
                isbreak= True
                break
            elif self.priority(op1)>=self.priority(op2):
                a=self.mgr.newOperator(op1,[a,b])
                op1=op2
            else:
                b = self.getExpression(a=b,op1=op2,_break=_break)
                expression= self.mgr.newOperator(op1,[a,b])
                isbreak= True
                break
        if not isbreak: expression=self.mgr.newOperator(op1,[a,b])
        # if all the operands are constant, reduce the expression a constant 
        if expression != None and hasattr(expression, 'operands'):
            allConstants=True              
            for p in expression.operands:
                if type(p).__name__ !=  'Constant':
                    allConstants=False
                    break
            if  allConstants:
                value = expression.value
                _type = type(value).__name__
                return Constant(value,_type)
        return expression             

    def getOperand(self):        
        isNegative=False
        isNot=False
        isBitNot=False
        operand=None
        char = self.current
        if char == '-':
           isNegative=True
           self.index+=1
           char = self.current
        elif char == '~':
           isBitNot=True
           self.index+=1
           char = self.current            
        elif char == '!':
           isNot=True
           self.index+=1
           char = self.current   

        if char.isalnum():    
            value=  self.getValue()
            if not self.end and self.current == '(':
                self.index+=1
                args=  self.getArgs(end=')')
                if '.' in value:
                    names = value.split('.')
                    key = names.pop()
                    variableName= '.'.join(names)
                    variable = Variable(variableName)
                    args.insert(0,variable)
                    operand= Function(self.mgr,key,args,True)
                else:
                    operand= Function(self.mgr,value,args)       

            elif not self.end and self.current == '[':
                self.index+=1    
                idx= self.getExpression(_break=']')
                operand= Variable(value)
                operand = IndexDecorator(operand,idx)                
            elif self.reInt.match(value): 
                if isNegative:
                    value = int(value)* -1
                    isNegative= False 
                elif isBitNot:
                    value = ~ int(value)
                    isBitNot= False     
                else:
                    value =int(value)
                operand = Constant(value,'int')
            elif self.reFloat.match(value):
                if isNegative:
                    value = float(value)* -1
                    isNegative= False
                elif isBitNot:
                    value = ~float(value)
                    isBitNot= False      
                else:
                    value =float(value)
                operand = Constant(value,'float')
            elif value=='true':                
                 operand = Constant(True,type(True))
            elif value=='false':                
                 operand = Constant(False,type(False))          
            elif self.mgr.isEnum(value):                
                if '.' in value and self.mgr.isEnum(value):
                    names = value.split('.')
                    enumName = names[0]
                    enumOption = names[1] 
                    enumValue= self.mgr.getEnumValue(enumName,enumOption)
                    enumType = type(enumValue).__name__
                    operand = Constant(enumValue,enumType)
                else:
                    values= self.mgr.getEnum(value)
                    attributes= []
                    for name in values:
                        _value = values[name]
                        _valueType = type(_value).__name__
                        attribute = KeyValue(name,Constant(_value,_valueType))
                        attributes.append(attribute)
                    operand= Object(attributes)
            else:
                operand = Variable(value)
        elif char == '\'' or char == '"':
            self.index+=1
            result=  self.getString(char)
            operand= Constant(result,'str')
        elif char == '(':
            self.index+=1
            operand=  self.getExpression(_break=')') 
        elif char == '{':
            self.index+=1
            operand = self.getObject()  
        elif char == '[':
            self.index+=1
            elements=  self.getArgs(end=']')
            operand = Array(elements)

        if not self.end and  self.current=='.':
            self.index+=1
            function= self.getOperand()
            function.operands.insert(0,operand)
            function.isChild = True
            operand=function

        if isNegative:operand=NegativeDecorator(operand)
        if isNot:operand=NotDecorator(operand)
        if isBitNot:operand=BitNot(operand)  
        return operand

    def priority(self,op):
        return self.mgr.priority(op)        

    def getValue(self):
        buff=[]
        while not self.end and self.reAlphanumeric.match(self.current):
            buff.append(self.current)
            self.index+=1
        return ''.join(buff)

    def getOperator(self):
        if self.end:return None 
        op=None
        if self.index+2 < self.length:
            triple = self.current+self.next+self.chars[self.index+2]
            if triple in self.mgr.tripleOperators :op=triple
            # if triple in ['**=','//=','<<=','>>=']:op=triple
        if op is None and  self.index+1 < self.length:
            double = self.current+self.next
            if double in self.mgr.doubleOperators  :op=double
            # if double in ['**','//','>=','<=','!=','==','+=','-=','*=','/=','%=','&&','||','|=','^=','<<','>>']  :op=double
        if op is None:op=self.current 
        self.index+=len(op)
        return op

    def getString(self,char):
        buff=[]       
        while not self.end :
            if self.current == char:
                if not((self.index+1 < self.length and self.next == char) or (self.previous == char)):
                    break 
            buff.append(self.current)
            self.index+=1
        self.index+=1    
        return ''.join(buff)

    def getArgs(self,end=')'):
        args= []
        while True:
            arg= self.getExpression(_break=','+end)
            if arg != None:args.append(arg)
            if self.previous==end: break
        return args

    def getObject(self):
        attributes= []
        while True:
            name= self.getValue()
            if self.current==':':self.index+=1
            else:raise ExpressionError('attribute '+name+' without value')
            value= self.getExpression(_break=',}')
            attribute = KeyValue(name,value)
            attributes.append(attribute)
            if self.previous=='}':
                self.index+=1 
                break
        
        return Object(attributes) 