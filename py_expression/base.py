from enum import Enum
import uuid
from datetime import date,datetime,time,timedelta 
import inspect

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ModelException(Exception):pass
class ExpressionException(Exception):pass
class Debug(Exception):pass

class Model():
    def __init__(self):
        self._operators={}
        self._enums={} 
        self._functions={}

    @property
    def enums(self):
        return self._enums
    @property
    def operators(self):
        return self._operators
    @property
    def functions(self):
        return self._functions

    def addEnum(self,key,source):
        self.enums[key]=source
    def isEnum(self,name):    
        names = name.split('.')
        return names[0] in self.enums.keys()
    def getEnumValue(self,name,option): 
        return self.enums[name][option]
    def getEnum(self,name): 
        return self.enums[name]
  
    def addOperator(self,name:str,cardinality:int,metadata):
        if name not in self.operators.keys():self.operators[name]= {}    
        self.operators[name][cardinality] = metadata       

    def addFunction(self:str,name:str,metadata):
        self.functions[name] = metadata    
    
    def getOperatorMetadata(self,name:str,cardinality:int):
        try:            
            if name in self._operators:
                operator = self._operators[name]
                if cardinality in operator:
                    return operator[cardinality]
            return None        
        except:
            raise ModelException('error with operator: '+name)     

    def getFunctionMetadata(self,name:str):
        try:
            if name in self._functions:
                return self._functions[name]
            return None
        except:
            raise ModelException('error with function: '+name)        
        
class Library():
    def __init__(self,name):
        self._name = name
        self._enums={} 
        self._operators={}
        self._functions={}

    @property
    def name(self):
        return self._name

    @property
    def enums(self):
        return self._enums

    @property
    def operators(self):
        return self._operators 

    @property
    def functions(self):
        return self._functions
 
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
            raise ModelException('enum not supported: '+key)    

    def addOperator(self,name:str,category:str,source,priority:int=-1,custom=None,customFunction=None):
        if name not in self._operators.keys():
            self._operators[name]= {}

        metadata = self.getMetadata(source)
        metadata['lib'] =self._name   
        metadata['category'] =category
        metadata['priority'] =priority
        cardinality = len(metadata['args'])    
        self._operators[name][cardinality]={'function':source,'metadata':metadata,'custom':custom,'customFunction':customFunction}

    def addFunction(self,name,source,custom=None,isArrowFunction:bool=False):        
        metadata = self.getMetadata(source)
        metadata['lib'] =self._name  
        metadata['isArrowFunction'] =isArrowFunction        
        self._functions[name]={'function':source,'metadata':metadata,'custom':custom} 

    def getFunction(self,name):
        if name in self._functions:
            return self._functions[name]
        return None

    def getMetadata(self,source):
        signature= inspect.signature(source)
        args=[]
        _signature = ''
        for parameter in signature.parameters.values():
            _type = self.getType(parameter.annotation)
            _default = self.getDefault(parameter.default)
            arg = {'name':parameter.name
                  ,'type': _type
                  ,'default':_default
                  }
            args.append(arg)
            _signature+= ('' if _signature=='' else ',')+(parameter.name)+(':'+_type if _type is not None else '' )+( '='+_default if _default is not None else '')    

        returnType = self.getType(signature.return_annotation)        
        return {
            'originalName': source.__name__,
            'signature': '('+_signature+')'+ ( '->'+returnType if returnType is not None else ''),
            'doc':source.__doc__,
            'args': args,
            'return':returnType
        }

    def getDefault(self,default):
        if str(default) == "<class 'inspect._empty'>": return None
        return str(default)     
    def getType(self,annotation):
        _type = inspect.formatannotation(annotation)
        if(_type == '<built-in function any>'):return 'any'
        elif (_type == 'inspect._empty'):return None
        return _type

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

class ChildContextable(Contextable):pass

class Token():
    def __init__(self):
        self._id= str(uuid.uuid4())
        self._stack = {}
        self._isBreak= False
        self._listeners = [] 
        self._signals = [] 

    @property
    def id(self): 
        return self._id

    @property
    def stack(self): 
        return self._stack
    @stack.setter
    def stack(self,value):
        self._stack =value 
    
    @property
    def listeners(self):
        return self._listeners 

    def addListener(self,value):
        self._isBreak = True 
        self._listeners.append(value)

    def clearListeners(self):
        self._isBreak = False 
        self._listeners = []    

    @property
    def signals(self):
        return self._signals 

    def addSignal(self,value):
        self._signals.append(value)

    def clearSignals(self):
        self._signals = []     

    @property
    def isBreak(self):
        return self._isBreak  
    @isBreak.setter
    def isBreak(self,value):
        self._isBreak =value             

class Step():
    def __init__(self,name,index,level):
        self._name = name
        self._index = index
        self._level = level
        self._values = []

    @property
    def values(self): 
        return self._values

class Value():
    def __init__(self,value=None):
        self._value= value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value =value      

class Node():
    def __init__(self,name,type,children=[]): 
        self._name = name
        self._type = type         
        self._children  = children
        self._parent = None
        self._index = None

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name =value    

    @property
    def type(self):
        return self._type 
    @type.setter
    def type(self,value):
        self._type =value         
    
    @property
    def children(self):
        return self._children 

    @property
    def parent(self):
        return self._parent 
    @parent.setter
    def parent(self,value):
        self._parent =value  

    @property
    def index(self):
        return self._index 
    @index.setter
    def index(self,value):
        self._index =value      
    

    def __add__(self, other):return Node('+','operator',[other,self]) 
    def __sub__(self, other):return Node('-','operator',[other,self])    
    def __mul__(self, other):return Node('*','operator',[other,self])
    def __pow__(self, other):return Node('**','operator',[other,self]) 
    def __truediv__(self, other):return Node('/','operator',[other,self]) 
    def __floordiv__(self, other):return Node('//','operator',[other,self]) 
    def __mod__(self, other):return Node('%','operator',[other,self])

    def __lshift__(self, other):return Node('<<','operator',[other,self])
    def __rshift__(self, other):return Node('>>','operator',[other,self])
    def __and__(self, other):return Node('&','operator',[other,self])
    def __or__(self, other):return Node('|','operator',[other,self])
    def __xor__(self, other):return Node('^','operator',[other,self])
    def __invert__(self, other):return Node('~','operator',[other,self])

    def __lt__(self, other):return Node('<','operator',[other,self])
    def __le__(self, other):return Node('<=','operator',[other,self])
    def __eq__(self, other):return Node('==','operator',[other,self])
    def __ne__(self, other):return Node('!=','operator',[other,self])
    def __gt__(self, other):return Node('>','operator',[other,self])
    def __ge__(self, other):return Node('>=','operator',[other,self])

    def __not__(self):return Node('!','operator',[self])
    def __and2__(self, other):return Node('&&','operator',[other,self])
    def __or2__(self, other):return Node('||','operator',[other,self])

    def __isub__(self, other):return Node('-=','operator',[other,self])
    def __iadd__(self, other):return Node('+=','operator',[other,self])
    def __imul__(self, other):return Node('*=','operator',[other,self])
    def __idiv__(self, other):return Node('/=','operator',[other,self])
    def __ifloordiv__(self, other):return Node('//=','operator',[other,self])
    def __imod__(self, other):return Node('%=','operator',[other,self])
    def __ipow__(self, other):return Node('**=','operator',[other,self])   

class Signal():
    def __init__(self,key:str,datetime:datetime=None):
        self._key= key
        self._datetime= datetime

    @property
    def key(self)->str:
        return self._key

    @property
    def datetime(self)->datetime:
        return self._datetime    

class WaitSignal(Signal):
    def __init__(self,name:str,secs:float=None):
        super(WaitSignal,self).__init__(name) 
        self._secs = secs  

    @property
    def secs(self):
        return self._secs 


class Operand():
    def __init__(self,name:str,children:list['Operand']=[]):
        self._name = name        
        self._children  = children
        self._id = None
        self._parent = None
        self._index = 0
        self._level = 0

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name =value    

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,value):
        self._id =value    

    @property
    def parent(self):
        return self._parent 
    @parent.setter
    def parent(self,value):
        self._parent =value  

    @property
    def index(self):
        return self._index 
    @index.setter
    def index(self,value):
        self._index =value      

    @property
    def level(self):
        return self._level 
    @level.setter
    def level(self,value):
        self._level =value      


    @property
    def children(self):
        return self._children 

    def eval(self,token:Token)->Value:
        values=None
        # add element to stack if not exist and get values
        if not self._id in token.stack:
            step = Step(self._name,self._index,self._level)
            values = step.values
            token.stack[self._id] = step
        else:
            values = token.stack[self._id].values  
        # solve operation
        result=self.solve(values,token)

        if token.isBreak:
            return result
        else:    
            # remove stack
            del token.stack[self._id]            
            return result 

    def solve(self,values,token:Token)->Value:pass



class Constant(Operand):
    def __init__(self,name,children=[]):
      super(Constant,self).__init__(name,children)  
      self._type  = type(name).__name__

    @property
    def type(self): 
        return self._type  

    def solve(self,values,token:Token)->Value:
        return Value(self._name)

class Variable(Operand,Contextable):
    def __init__(self,name:str,children:list[Operand]=[]):
        Operand.__init__(self,name,children)

    def solve(self,values,token:Token)->Value:
        return Value(self.context.get(self._name))

    def set(self,value,token:Token):
        self.context.set(self._name,value)    
    
class KeyValue(Operand):
    def solve(self,values,token:Token)->Value:
        return self._children[0].eval(token)

class Array(Operand):
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value   
                values.append(value.value)
        return Value(values)       

class Object(Operand):
    def solve(self,values,token:Token)->Value:
        
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        dic= {}
        for i,value in enumerate(values):
            dic[self._children[i].name]=value
        return Value(dic)     

class Operator(Operand):
    def __init__(self,name:str,children:list[Operand]=[],function=None):
        super(Operator,self).__init__(name,children) 
        self._function = function
  
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(self._function(*values))                 
                              
class Function(Operand):
    def __init__(self,name:str,children:list[Operand]=[],function=None):
        super(Function,self).__init__(name,children) 
        self._function = function

    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(self._function(*values))   

class ArrowFunction(Function,ChildContextable):pass

class ContextFunction(Function):
    def solve(self,values,token:Token)->Value:
        if len(values) == 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value 
            values.append()
        if isinstance(values[0],object) and hasattr(values[0], self._name):
            function=getattr(values[0], self._name)
            for i,p in enumerate(self._children[1:]):
                if i >= len(values):
                    value = p.eval(token)
                    if token.isBreak: return value 
                    values.append(value.value)
            return Value(function(*values[1:]))     
        else:    
            raise ExpressionException('function: '+self._name +' not found in') 

class Block(Operand):
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(values)          
                
class If(Operand):
    def solve(self,values,token:Token)->Value:
        if len(values)== 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        if values[0]:
            value = self._children[1].eval(token)
            if token.isBreak: return value
            values.append(value.value) 
        elif len(self._children) > 2 and self._children[2] is not None:
            value = self._children[2].eval(token)
            if token.isBreak: return value
            values.append(value.value)         
        return Value(values)         
         
class While(Operand):
    def solve(self,values,token:Token)->Value:
        if len(values)== 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        while values[0]:
            if len(values) < 2:
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)

            values = []
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        return Value(None)          
           

       
        
