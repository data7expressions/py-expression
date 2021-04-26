import re
import math
import time as t
from datetime import date,datetime,time,timedelta
# import pytz
from os import path,getcwd
from enum import Enum
# from .base import *

class Context():
    def __init__(self,data:dict={},parent:'Context'=None):
        self.data = data
        self._parent= parent

    def newContext(self):        
        return Context({},self)

    def getConext(self,variable):
        if variable in self.data or self._parent is None: return self.data
        _context =self._parent.getConext(variable)
        return _context  if _context is not None else self.data

    def get(self,name):
        names=name.split('.')
        value = self.getConext(names[0]) 
        for n in names:
            if n not in value: return None
            value=value[n]
        return value

    def set(self,name,value):
        names=name.split('.')        
        level = len(names)-1
        list = self.getConext(names[0]) 
        for i,e in enumerate(names):
            if i == level:
                list[e]=value
            else:                    
                list=list[e] 

    def init(self,name,value):
        self.data[name]=value                     

class Contextable():
    def __init__(self):
      self._context  = None

    @property
    def context(self):
        return self._context
    @context.setter
    def context(self,value):
        self._context=value

class Managerable():
    def __init__(self):
      self._mgr  = None

    @property
    def mgr(self):
        return self._mgr
    @mgr.setter
    def mgr(self,value):
        self._mgr=value 

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ExpressionError(Exception):pass

class Token():
    def __init__(self):
        self._value = None
        self._path = []

    @property
    def value(self): 
        return self._value
    @value.setter
    def value(self,value):
        self._value =value  

    @property
    def path(self): 
        return self._path
    @path.setter
    def path(self,value):
        self._path =value         

class Operand():
    def __init__(self,name,operands=[]): 
        self._name = name         
        self._operands  = operands
        self._parent = None 

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name =value    

    @property
    def parent(self):
        return self._parent 
    @parent.setter
    def parent(self,value):
        self._parent =value       

    @property
    def value(self): 
        pass   

    @property
    def operands(self):
        return self._operands 

    def __add__(self, other):return Exp().newOperator('+',[other,self]) 
    def __sub__(self, other):return Exp().newOperator('-',[other,self])    
    def __mul__(self, other):return Exp().newOperator('*',[other,self])
    def __pow__(self, other):return Exp().newOperator('**',[other,self]) 
    def __truediv__(self, other):return Exp().newOperator('/',[other,self]) 
    def __floordiv__(self, other):return Exp().newOperator('//',[other,self]) 
    def __mod__(self, other):return Exp().newOperator('%',[other,self])

    def __lshift__(self, other):return Exp().newOperator('<<',[other,self])
    def __rshift__(self, other):return Exp().newOperator('>>',[other,self])
    def __and__(self, other):return Exp().newOperator('&',[other,self])
    def __or__(self, other):return Exp().newOperator('|',[other,self])
    def __xor__(self, other):return Exp().newOperator('^',[other,self])
    def __invert__(self, other):return Exp().newOperator('~',[other,self])

    def __lt__(self, other):return Exp().newOperator('<',[other,self])
    def __le__(self, other):return Exp().newOperator('<=',[other,self])
    def __eq__(self, other):return Exp().newOperator('==',[other,self])
    def __ne__(self, other):return Exp().newOperator('!=',[other,self])
    def __gt__(self, other):return Exp().newOperator('>',[other,self])
    def __ge__(self, other):return Exp().newOperator('>=',[other,self])

    def __not__(self):return Exp().newOperator('!',[self])
    def __and2__(self, other):return Exp().newOperator('&&',[other,self])
    def __or2__(self, other):return Exp().newOperator('||',[other,self])

    def __isub__(self, other):return Exp().newOperator('-=',[other,self])
    def __iadd__(self, other):return Exp().newOperator('+=',[other,self])
    def __imul__(self, other):return Exp().newOperator('*=',[other,self])
    def __idiv__(self, other):return Exp().newOperator('/=',[other,self])
    def __ifloordiv__(self, other):return Exp().newOperator('//=',[other,self])
    def __imod__(self, other):return Exp().newOperator('%=',[other,self])
    def __ipow__(self, other):return Exp().newOperator('**=',[other,self])


    def debug(self,token:Token,level): 
        if len(token.path) <= level:
            if len(self.operands)== 0:
                token.value= self.value 
            else:
                token.path.append(0)
                self.operands[0].debug(token,level+1)   
        else:
            idx = token.path[level]
            # si es el anteultimo nodo 
            if len(token.path) -1 == level:           
                if len(self.operands) > idx+1:
                   token.path[level] = idx+1
                   self.operands[idx+1].debug(token,level+1)
                else:
                   token.path.pop() 
                   token.value= self.value       
            else:
                self.operands[idx].debug(token,level+1)
        
  
    def eval(self,context:dict=None):
        return Exp().eval(self,context)
    def vars(self):
        return Exp().getVars(self)
    def constants(self):
        return Exp().getConstants(self) 
    def operators(self):
        return Exp().getOperators(self)
    def functions(self):
        return Exp().getFunctions(self)

class Constant(Operand):
    def __init__(self,name,operands=[]):
      super(Constant,self).__init__(name)  
    #   self._value  = name
      self._type  = type(name).__name__

    @property
    def value(self): 
        return self.name
    @property
    def type(self): 
        return self._type     

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self.name)  

class Variable(Operand,Contextable):
    def __init__(self,name,operands=[]):
      Operand.__init__(self,name,operands) 
      self._names = name.split('.')

    @property
    def value(self):
        return self._context.get(self.name)

    @value.setter
    def value(self,value):
        self._context.set(self.name,value)

    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name      
class KeyValue(Operand):
    def __init__(self,name,operands=[]):
        super(KeyValue,self).__init__(name,operands)

    @property
    def value(self): 
        return self._operands[0].value
class Array(Operand):
    def __init__(self,name,operands=[]):
      super(Array,self).__init__(name,operands)

    @property
    def value(self):
        list= []
        for p in self._operands:
            list.append(p.value)
        return list 
class Object(Operand):
    def __init__(self,name,operands=[]):
      super(Object,self).__init__(name,operands)

    @property
    def value(self):
        dic= {}
        for p in self._operands:
            dic[p.name]=p.value
        return dic

class ArrayForeach(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        for p in variable.value:
            childContext.init(self.name,p)
            body.value
class ArrayMap(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        result=[]
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        for p in variable.value:
            childContext.init(self.name,p)
            result.append(body.value)
        return result
class ArrayFirst(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        for p in variable.value:
            childContext.init(self.name,p)
            if body.value : return p
        return None
class ArrayLast(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        value = variable.value
        value.reverse()
        for p in value:
            childContext.init(self.name,p)
            if body.value : return p
        return None 
class ArrayFilter(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        result=[]
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        for p in variable.value:
            childContext.init(self.name,p)
            if body.value: result.append(p)
        return result        
class ArrayReverse(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        if len(self._operands)==1:
            variable= self._operands[0]
            value = variable.value
            value.reverse()
            return value
        else:
            result=[]
            variable= self._operands[0]
            method= self._operands[1]
            childContext=self.context.newContext()
            self.mgr.setContext(method,childContext)
            for p in variable.value:
                childContext.init(self.name,p)
                result.append({"ord":method.value,"p":p})
            result.sort((lambda p: p["ord"]))
            result.reverse()    
            return map(lambda p: p['p'],result)
class ArraySort(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):
        if len(self._operands)==1:
            variable= self._operands[0]
            value = variable.value
            value.reverse()
            return value
        else:
            result=[]
            variable= self._operands[0]
            method= self._operands[1]
            childContext=self.context.newContext()
            self.mgr.setContext(method,childContext)
            for p in variable.value:
                childContext.init(self.name,p)
                result.append({"ord":method.value,"p":p})
            result.sort((lambda p: p["ord"]))
            return map(lambda p: p['p'],result)
class ArrayPush(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):        
        variable= self._operands[0]
        elemnent= self._operands[1]
        value = variable.value
        value.append(elemnent)
        return value
class ArrayPop(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):        
        variable= self._operands[0]
        index =None
        if len(self._operands)>1:
            index= self._operands[1].value
        else:
            index = len(self._operands) -1        
        return variable.value.pop(index)
class ArrayRemove(Operand,Contextable,Managerable):
    def __init__(self,name,operands=[]):
        Operand.__init__(self,name,operands)

    @property
    def value(self):        
        variable= self._operands[0]
        element= self._operands[1]
        variable.value.remove(element.value)    

class Function(Operand,Managerable):
    def __init__(self,name,operands=[]):
      Operand.__init__(self,name,operands)

    @property
    def value(self): 
        args=[]
        if '.' in self.name:
            name = self.name.replace('.','')
            parent = self._operands.pop(0)
            value = parent.value
            _type = type(value).__name__
            if isinstance(value,object) and hasattr(value, name):
                function=getattr(value, name)
                for p in self._operands:args.append(p.value)
            else:    
                function=self._mgr.getFunction(name,_type)            
                for p in self._operands:args.append(p.value)
                args.insert(0,value)            
        else:
            function=self._mgr.getFunction(self.name)
            for p in self._operands:args.append(p.value)
        return function(*args)
class Block(Operand):
    def __init__(self,name,elements=[]):
      super(Block,self).__init__(name,elements)

    @property
    def value(self):        
        for p in self._operands:
            p.value

    # TODO
    def debug(self,token:Token,level): 
        pass              
class If(Operand):
    def __init__(self,name,operands=[]):
      super(If,self).__init__(name,operands)      

    @property
    def value(self):         
        if self.operands[0].value:
           self.operands[1].value
        elif len(self.operands) > 2 and self.operands[2] is not None:       
            self.operands[2].value

    # TODO
    def debug(self,token:Token,level): 
        pass          
class While(Operand):
    def __init__(self,name,operands=[]):
      super(While,self).__init__(name,operands)      

    @property
    def value(self): 
        while self.operands[0].value:
           self.operands[1].value

    # TODO
    def debug(self,token:Token,level): 
        pass        
class Operator(Operand):
    def __init__(self,name,operands=[]):
      super(Operator,self).__init__(name,operands)

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
    def __init__(self,name,operands=[] ):
        super(NegativeDecorator,self).__init__(name,operands)

    @property
    def value(self): 
        return self._operands[0].value * -1
class NotDecorator(Operator):
    def __init__(self,name,operands=[]):
      super(NotDecorator,self).__init__(name,operands)

    @property
    def value(self): 
        return not self._operands[0].value 
class IndexDecorator(Operator):
    def __init__(self,name,operands=[] ):
      super(IndexDecorator,self).__init__(name,operands)        

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

    # TODO
    def debug(self,token:Token,level): 
        pass 
class Or(Operator):
    @property
    def value(self):
        if self._operands[0].value : return True
        return self._operands[1].value
    # TODO
    def debug(self,token:Token,level): 
        pass 
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
       
   
class Exp(metaclass=Singleton):
    def __init__(self):
       self.reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$') 
       self.reInt = re.compile('[0-9]+$')
       self.reFloat = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')
       self._operators={}
       self._tripleOperators = []
       self._doubleOperators = [] 
       self._enums={} 
       self._functions={}
       self.initOperators()
       self.generalFunctions()
       self.mathFunctions()
       self.datetimeFunctions()
       self.stringFunctions()
       self.ioFunctions()
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
        self.addFunction('nvl',lambda a,b: a if a!=None and a!="" else b )
        self.addFunction('isEmpty',lambda a: a==None or a =="")
        self.addFunction('sleep',t.sleep)        
      
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
    
    def datetimeFunctions(self):
        # https://stackabuse.com/how-to-format-dates-in-python/
        # https://www.programiz.com/python-programming/datetime

        self.addFunction('strftime',datetime.strftime,['datetime'])
        self.addFunction('strptime',datetime.strptime)        
        self.addFunction('datetime',datetime)
        self.addFunction('today',date.today)
        self.addFunction('now',datetime.now)
        self.addFunction('date',date)
        self.addFunction('fromtimestamp',date.fromtimestamp)
        self.addFunction('time',time)
        self.addFunction('timedelta',timedelta)
        # self.addFunction('timezone',pytz.timezone) 

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

    def ioFunctions(self): 
        class Volume():
            def __init__(self,_path):        
                self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
            def fullpath(self,_path):
                return path.join(self._root,_path)
        def createVolume(_path):return Volume(_path)

        self.addFunction('Volume',createVolume)
        self.addFunction('pathRoot',getcwd)
        self.addFunction('pathJoin',path.join)

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
            return operator["imp"](key,operands)
        except:
            raise ExpressionError('error with operator: '+str(key))  
    def priority(self,key):
        return self._operators[key]["priority"] if key in self._operators else -1          
    def addOperator(self,key:str,category:str,source:Operator,priority:int=-1):        
        self._operators[key]={"category":category,"priority":priority,"imp":source}
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
    def addFunction(self,name,source,types=['any']):
        if name not in self._functions.keys():
            self._functions[name]= []
        self._functions[name].append({'types':types,'imp':source})         
    def getFunction(self,key,type='any'):
        for p in self._functions[key]:
            if type in p['types']:
                return p['imp']
        return None    
    
    def minify(self,expression:str)->str:
        isString=False
        quotes=None
        result =[]
        buffer = list(expression)
        for p in buffer:
            if isString and p == quotes: isString=False 
            elif not isString and (p == '\'' or p=='"'):
                isString=True
                quotes=p
            if (p != ' ' and p!='\n' and p!='\r' and p!='\t' ) or isString:
               result.append(p)
        return result
    
    def parse(self,expression)->Operand:
        try:            
            parser = Parser(self,self.minify(expression))
            operand= parser.parse() 
            del parser
            return operand  
        except Exception as error:
            raise ExpressionError('expression: '+expression+' error: '+str(error))

    def eval(self,operand:Operand,context:dict={})-> any :  
        if context is not None:
            self.setContext(operand,Context(context))
        return operand.value

    def debug(self,operand:Operand,token:Token,context:dict={}):
        if context is not None:
            self.setContext(operand,Context(context))
        operand.debug(token,0)

    def solve(self,expression:str,context:dict={})-> any :
        operand=self.parse(expression)
        return self.eval(operand,context)

    def serialize(self,operand:Operand)-> dict:        
        if len(operand.operands)==0:return {'n':operand.name,'t':type(operand).__name__}
        children = []                
        for p in operand.operands:
            children.append(self.serialize(p))
        return {'n':operand.name,'t':type(operand).__name__,'c':children}     

    def deserialize(self,serialized:dict)-> Operand:
        children = []
        if 'c' in serialized:
            for p in serialized['c']:
                children.append(self.deserialize(p))
        return  eval(serialized['t'])(serialized['n'],children) 

 
    def getOperandByPath(self,operand:Operand,path)->Operand:
        search = operand
        for p in path:
            if len(search.operands) <= p:return None
            search = search.operands[p]
        return search    

        
    def setContext(self,operand:Operand,context:Context):
        if issubclass(operand.__class__,Contextable):operand.context = context 
        if issubclass(operand.__class__,Managerable):operand.mgr = self
        if len(operand.operands)>0 :       
            for p in operand.operands:
                if issubclass(p.__class__,Contextable):p.context = context
                if issubclass(p.__class__,Managerable):p.mgr = self 
                if len(p.operands)>0:
                    self.setContext(p,context)

    def setParent(self,expression:Operand,parent:Operand=None):
        expression.parent = parent
        if  len(expression.operands)>0: 
            for p in expression.operands:
                self.setParent(p,expression)        


    def getVars(self,expression:Operand)->dict:
        list = {}
        if type(expression).__name__ ==  'Variable':
            list[expression.name] = "any"
        for p in expression.operands:
            if type(p).__name__ ==  'Variable':
                list[p.name] = "any"
            elif len(p.operands)>0:
                subList= self.getVars(p)
                list = {**list, **subList}
        return list        
    def getConstants(self,expression:Operand)->dict:
        list = {}
        if type(expression).__name__ ==  'Constant':
            list[expression.value] = expression.type
        for p in expression.operands:
            if type(p).__name__ ==  'Constant':
                list[p.value] = p.type
            elif len(p.operands)>0:
                subList= self.getConstants(p)
                list = {**list, **subList}
        return list
    def getOperators(self,expression:Operand)->dict:
        list = {}
        if isinstance(expression,Operator):
            operator = self._operators[expression.name]; 
            list[expression.name] = operator['category']
        for p in expression.operands:
            if isinstance(p,Operator):
                operator = self._operators[p.name]; 
                list[p.name] =  operator['category']
            elif len(p.operands)>0:
                subList= self.getOperators(p)
                list = {**list, **subList}
        return list
    def getFunctions(self,expression:Operand)->dict:
        list = {}
        if type(expression).__name__ ==  'Function':list[expression.name] = {"isChild": '.' in expression.name}
        for p in expression.operands:
            if type(p).__name__ ==  'Function':list[p.name] =  {"isChild": '.' in p.name}
            elif len(p.operands)>0:
                subList= self.getFunctions(p)
                list = {**list, **subList}
        return list
    def functionInfo(self,key):
        if key not in self._functions: return None
        info=[]
        for p in self._functions[key]:
            info.append({'types':p['types']})
        return info;
 
class Parser():
    def __init__(self,mgr,expression):
       self.mgr = mgr 
       self.buffer = list(expression)
       self.length=len(self.buffer)
       self.index=0
    
    def parse(self):
        operands=[]
        while not self.end:
            operand =self.getExpression(_break=';')
            if operand is None:break
            operands.append(operand)
        if len(operands)==1 :
            return operands[0]
        return Block('block',operands) 

    @property
    def previous(self):
        return self.buffer[self.index-1] 
    @property
    def current(self):
        return self.buffer[self.index]    
    @property
    def next(self):
        return self.buffer[self.index+1]
    @property
    def end(self):
        return self.index >= self.length   

    def getExpression(self,operand1=None,operator=None,_break=''):
        expression = None
        operand2 = None
        isbreak = False               
        while not self.end:
            if operand1 is None and operator is None: 
                operand1=  self.getOperand()
                operator= self.getOperator()
                if operator is None or operator in _break: 
                    expression = operand1
                    isbreak= True
                    break
            operand2=  self.getOperand()
            nextOperator= self.getOperator()
            if nextOperator is None or nextOperator in _break:
                expression= self.mgr.newOperator(operator,[operand1,operand2])
                isbreak= True
                break
            elif self.priority(operator)>=self.priority(nextOperator):
                operand1=self.mgr.newOperator(operator,[operand1,operand2])
                operator=nextOperator
            else:
                operand2 = self.getExpression(operand1=operand2,operator=nextOperator,_break=_break)
                expression= self.mgr.newOperator(operator,[operand1,operand2])
                isbreak= True
                break
        if not isbreak: expression=self.mgr.newOperator(operator,[operand1,operand2])
        # if all the operands are constant, reduce the expression a constant 
        if expression is not None and len(expression.operands)>0:    
            allConstants=True              
            for p in expression.operands:
                if type(p).__name__ !=  'Constant':
                    allConstants=False
                    break
            if  allConstants:
                value = expression.value                
                return Constant(value)
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
            if value=='if' and self.current == '(': 
                self.index+=1
                operand = self.getIfBlock()
            elif value=='while' and self.current == '(': 
                self.index+=1
                operand = self.getWhileBlock()            
            elif not self.end and self.current == '(':
                self.index+=1
                if '.' in value:
                    names = value.split('.')
                    name = names.pop()
                    variableName= '.'.join(names)
                    variable = Variable(variableName)
                    operand= self.getChildFunction(name,variable)
                else:
                    args=  self.getArgs(end=')')
                    operand= Function(value,args)                

            elif not self.end and self.current == '[':
                self.index+=1    
                operand = self.getIndexOperand(value)              
            elif self.mgr.reInt.match(value): 
                if isNegative:
                    value = int(value)* -1
                    isNegative= False 
                elif isBitNot:
                    value = ~ int(value)
                    isBitNot= False     
                else:
                    value =int(value)
                operand = Constant(value)
            elif self.mgr.reFloat.match(value):
                if isNegative:
                    value = float(value)* -1
                    isNegative= False
                elif isBitNot:
                    value = ~float(value)
                    isBitNot= False      
                else:
                    value =float(value)
                operand = Constant(value)
            elif value=='true':                
                operand = Constant(True)
            elif value=='false':                
                operand = Constant(False)
            elif self.mgr.isEnum(value):                
                operand= self.getEnum(value)
            else:
                operand = Variable(value)
        elif char == '\'' or char == '"':
            self.index+=1
            result=  self.getString(char)
            operand= Constant(result)
        elif char == '(':
            self.index+=1
            operand=  self.getExpression(_break=')') 
        elif char == '{':
            self.index+=1
            operand = self.getObject()  
        elif char == '[':
            self.index+=1
            elements=  self.getArgs(end=']')
            operand = Array('array',elements)

        if not self.end and  self.current=='.':
            self.index+=1
            name=  self.getValue()
            if self.current == '(': self.index+=1
            operand =self.getChildFunction(name,operand)

            # function= self.getOperand()
            # function.operands.insert(0,operand)
            # if '.' not in function.name :function.name = '.'+function.name
            # operand=function

        if isNegative:operand=NegativeDecorator('-',[operand])
        if isNot:operand=NotDecorator('!',[operand])
        if isBitNot:operand=BitNot('~',[operand])  
        return operand

    def priority(self,op):
        return self.mgr.priority(op)        

    def getValue(self,increment:bool=True):
        buff=[]
        if increment:
            while not self.end and self.mgr.reAlphanumeric.match(self.current):
                buff.append(self.current)
                self.index+=1
        else:
            index = self.index
            while not self.end and self.mgr.reAlphanumeric.match(self.buffer[index]):
                buff.append(self.buffer[index])
                index+=1        
        return ''.join(buff)

    def getOperator(self):
        if self.end:return None 
        op=None
        if self.index+2 < self.length:
            triple = self.current+self.next+self.buffer[self.index+2]
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
            if arg is not None:args.append(arg)
            if self.previous==end: break
        return args

    def getObject(self):
        attributes= []
        while True:
            name=None
            if self.current== '"' or  self.current == "'":
                char= self.current
                self.index+=1
                name= self.getString(char)
            else:    
                name= self.getValue()
            if self.current==':':self.index+=1
            else:raise ExpressionError('attribute '+name+' without value')
            value= self.getExpression(_break=',}')
            attribute = KeyValue(name,[value])
            attributes.append(attribute)
            if self.previous=='}':
                break
        
        return Object('object',attributes) 

    def getBlock(self):
        lines= []
        while True:
            line= self.getExpression(_break=';}')
            if line is not None :lines.append(line)
            if self.previous=='}':
                break        
        return Block('block',lines)     

    def getIfBlock(self):
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';') 

        nextValue=self.getValue(increment=False)
        elseblock=None
        if nextValue=='else':
            self.index+=len(nextValue)
            if  self.current == '{':
                self.index+=1  
                elseblock= self.getBlock()
            else:
                elseblock= self.getExpression(_break=';') 

        return If('if',[condition,block,elseblock]) 

    def getWhileBlock(self):
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';') 

        return While('while',[condition,block])   

    def getChildFunction(self,name,parent):
        if name == 'foreach': return self.getForeach(parent)
        elif name == 'map': return self.getMap(parent)
        elif name == 'reverse': return self.getReverse(parent)
        elif name == 'first': return self.getFirst(parent)
        elif name == 'last': return self.getLast(parent)
        elif name == 'filter': return self.getFilter(parent)
        else: 
            args=  self.getArgs(end=')')
            args.insert(0,parent)
            return Function('.'+name,args)

        # if '.' in name:
        #     names = name.split('.')
        #     key = names.pop()
        #     variableName= '.'.join(names)
        #     variable = Variable(variableName)
        #     if key == 'foreach': return self.getForeach(variable)
        #     elif key == 'map': return self.getMap(variable)
        #     elif key == 'reverse': return self.getReverse(variable)
        #     elif key == 'first': return self.getFirst(variable)
        #     elif key == 'last': return self.getLast(variable)
        #     elif key == 'filter': return self.getFilter(variable)
        #     else: 
        #         args=  self.getArgs(end=')')
        #         args.insert(0,variable)
        #         return Function('.'+key,args)
        # else:
        #     args=  self.getArgs(end=')')
        #     return Function(name,args)

    def getForeach(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('foreach without body')
        body= self.getExpression(_break=')')
        return ArrayForeach(name,[variable,body]) 

    def getMap(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('map without body')
        body= self.getExpression(_break=')')
        return ArrayMap(name,[variable,body])   

    def getReverse(self,variable): 
        if self.current == ')': self.index+=1       
        return ArrayReverse('',[variable]) 
        # if self.current==':':self.index+=1
        # else:raise ExpressionError('reverse without body')
        # body= self.getExpression(_break=')')
        # return Reverse(name,[variable,body])   

    def getFirst(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('first without body')
        body= self.getExpression(_break=')')
        return ArrayFirst(name,[variable,body])  

    def getLast(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('last without body')
        body= self.getExpression(_break=')')
        return ArrayLast(name,[variable,body])                   

    def getFilter(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('filter without body')
        body= self.getExpression(_break=')')
        return ArrayFilter(name,[variable,body])  

    def getIndexOperand(self,name):
        idx= self.getExpression(_break=']')
        operand= Variable(name)
        return IndexDecorator('[]',[operand,idx]) 

    def getEnum(self,value):
        if '.' in value and self.mgr.isEnum(value):
            names = value.split('.')
            enumName = names[0]
            enumOption = names[1] 
            enumValue= self.mgr.getEnumValue(enumName,enumOption)
            # enumType = type(enumValue).__name__
            return Constant(enumValue)
        else:
            values= self.mgr.getEnum(value)
            attributes= []
            for name in values:
                _value = values[name]
                # _valueType = type(_value).__name__
                attribute = KeyValue(name,[Constant(_value)])
                attributes.append(attribute)
            return Object('object',attributes)
   

                            