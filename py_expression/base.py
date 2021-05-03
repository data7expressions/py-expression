from enum import Enum 
import inspect

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ModelError(Exception):pass
class ExpressionError(Exception):pass

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
            raise ModelError('enum not supported: '+key)    

    def addOperator(self,name:str,category:str,source,priority:int=-1,evaluator=None):
        if name not in self._operators.keys():
            self._operators[name]= {}

        metadata = self.getMetadata(source)
        metadata['lib'] =self._name   
        metadata['category'] =category
        metadata['priority'] =priority
        cardinality = len(metadata['args'])    
        self._operators[name][cardinality]={'function':source,'evaluator':evaluator,'metadata':metadata}

    def addFunction(self,name,source,evaluator=None,isArrowFunction:bool=False):        
        metadata = self.getMetadata(source)
        metadata['lib'] =self._name  
        metadata['isArrowFunction'] =isArrowFunction        
        self._functions[name]={'function':source,'evaluator':evaluator,'metadata':metadata} 

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
        self._index = None
        self._evaluator = None        

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
    def index(self):
        return self._index 
    @index.setter
    def index(self,value):
        self._index =value  

    @property
    def evaluator(self):
        return self._evaluator
    @evaluator.setter
    def evaluator(self,value):
        self._evaluator =value       
    
    @property
    def operands(self):
        return self._operands 

    @property
    def value(self): 
        return self._evaluator.eval(self) 

    @value.setter
    def value(self,value):
        self._evaluator.set(self,value)

    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name    
     
    

    def __add__(self, other):return Operator('+',[other,self]) 
    def __sub__(self, other):return Operator('-',[other,self])    
    def __mul__(self, other):return Operator('*',[other,self])
    def __pow__(self, other):return Operator('**',[other,self]) 
    def __truediv__(self, other):return Operator('/',[other,self]) 
    def __floordiv__(self, other):return Operator('//',[other,self]) 
    def __mod__(self, other):return Operator('%',[other,self])

    def __lshift__(self, other):return Operator('<<',[other,self])
    def __rshift__(self, other):return Operator('>>',[other,self])
    def __and__(self, other):return Operator('&',[other,self])
    def __or__(self, other):return Operator('|',[other,self])
    def __xor__(self, other):return Operator('^',[other,self])
    def __invert__(self, other):return Operator('~',[other,self])

    def __lt__(self, other):return Operator('<',[other,self])
    def __le__(self, other):return Operator('<=',[other,self])
    def __eq__(self, other):return Operator('==',[other,self])
    def __ne__(self, other):return Operator('!=',[other,self])
    def __gt__(self, other):return Operator('>',[other,self])
    def __ge__(self, other):return Operator('>=',[other,self])

    def __not__(self):return Operator('!',[self])
    def __and2__(self, other):return Operator('&&',[other,self])
    def __or2__(self, other):return Operator('||',[other,self])

    def __isub__(self, other):return Operator('-=',[other,self])
    def __iadd__(self, other):return Operator('+=',[other,self])
    def __imul__(self, other):return Operator('*=',[other,self])
    def __idiv__(self, other):return Operator('/=',[other,self])
    def __ifloordiv__(self, other):return Operator('//=',[other,self])
    def __imod__(self, other):return Operator('%=',[other,self])
    def __ipow__(self, other):return Operator('**=',[other,self])


    # def debug(self,token:Token,level): 
    #     if len(token.path) <= level:
    #         if len(self.operands)== 0:
    #             token.value= self.value 
    #         else:
    #             token.path.append(0)
    #             self.operands[0].debug(token,level+1)   
    #     else:
    #         idx = token.path[level]
    #         # si es el anteultimo nodo 
    #         if len(token.path) -1 == level:           
    #             if len(self.operands) > idx+1:
    #                token.path[level] = idx+1
    #                self.operands[idx+1].debug(token,level+1)
    #             else:
    #                token.path.pop() 
    #                token.value= self.value       
    #         else:
    #             self.operands[idx].debug(token,level+1)
        
  
    # def eval(self,context:dict=None):
    #     return self.mgr.eval(self,context)
    # def vars(self):
    #     return self.mgr.getVars(self)
    # def constants(self):
    #     return self.mgr.getConstants(self) 
    # def operators(self):
    #     return self.mgr.getOperators(self)
    # def functions(self):
    #     return self.mgr.getFunctions(self)

class Constant(Operand):
    def __init__(self,name,operands=[]):
      super(Constant,self).__init__(name,operands)  
      self._type  = type(name).__name__

    @property
    def type(self): 
        return self._type  

class Variable(Operand,Contextable):
    def __init__(self,name,operands=[]):
      Operand.__init__(self,name,operands) 

class KeyValue(Operand):pass
class Array(Operand): pass
class Object(Operand): pass
class Operator(Operand):pass
class Function(Operand):pass
class ArrowFunctions(Operand,ChildContextable):
    def __init__(self,name,operands=[]):
      Operand.__init__(self,name,operands)

class ChildFunction(Operand):pass
class Block(Operand):pass
class If(Operand):pass          
class While(Operand):pass

class Evaluator():
    def eval(self,operand):
        pass
    def set(self,operand,value):
        pass

class ConstantEvaluator(Evaluator):
    def eval(self,operand):
        return operand.name

class VariableEvaluator(Evaluator):
    def eval(self,operand):
        return operand.context.get(operand.name)

    def set(self,operand,value):
        operand.context.set(operand.name,value)

class KeyValueEvaluator(Evaluator):
    def eval(self,operand):
        return operand.operands[0].value

class ArrayEvaluator(Evaluator):
    def eval(self,operand):
        list= []
        for p in operand.operands:
            list.append(p.value)
        return list 

class ObjectEvaluator(Evaluator):
    def eval(self,operand):
        dic= {}
        for p in operand.operands:
            dic[p.name]=p.value
        return dic

class FunctionEvaluator(Evaluator):
    def __init__(self,function=None):
      super(FunctionEvaluator,self).__init__()         
      self.function = function
       
    def eval(self,operand):        
        values= []
        for p in operand.operands:
            values.append(p.value)
        return self.function(*values)

class ContextFunctionEvaluator(Evaluator):
    def eval(self,operand):  
        args=[] 
        parent = operand.operands.pop(0)
        value = parent.value
        if isinstance(value,object) and hasattr(value, operand.name):
            function=getattr(value, operand.name)
            for p in operand.operands:
                args.append(p.value)
            return function(*args)     
        else:    
            raise ExpressionError('function: '+operand.name +' not found in '+parent.name)

class BlockEvaluator(Evaluator):
    def eval(self,operand):        
        for p in operand.operands:
            p.value
                
class IfEvaluator(Evaluator):
    def eval(self,operand):         
        if operand.operands[0].value:
           operand.operands[1].value
        elif len(operand.operands) > 2 and operand.operands[2] is not None:       
            operand.operands[2].value
         
class WhileEvaluator(Evaluator):
    def eval(self,operand):
        while operand.operands[0].value:
           operand.operands[1].value
