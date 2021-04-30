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

    def addOperator(self,name:str,category:str,source,priority:int=-1):
        if name not in self._operators.keys():
            self._operators[name]= {}

        metadata = self.getMetadata(source)
        metadata['lib'] =self._name   
        metadata['category'] =category
        metadata['priority'] =priority
        cardinality = len(metadata['args'])    
        self._operators[name][cardinality]={"source":source,"metadata":metadata}

    def addFunction(self,name,source,type='na'):
        if name not in self._functions.keys():
            self._functions[name]= {}

        metadata = self.getMetadata(source)
        metadata['lib'] =self._name     

        self._functions[name][type]={"source":source,"metadata":metadata} 

    def getFunction(self,name,type='na'):
        if name in self._functions:
            function = self._functions[name]
            if type in function:
                return function[type]
        return None

    def getMetadata(self,source):
        signature= inspect.signature(source)
        args=[]
        for parameter in signature.parameters.values():
            arg = {'name':parameter.name
                  ,'type': inspect.formatannotation(parameter.annotation)
                  ,'default':parameter.default 
                  }
            args.append(arg) 

        # TODO: resolver estos tipos como
        # inspect._empty : null
        # <built-in function any> ; any    
        return {
            'name': source.__name__,
            'doc':source.__doc__,
            'args': args,
            'return':inspect.formatannotation(signature.return_annotation)
        }     

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
    def __init__(self,name,operands=[],mgr=None): 
        self._name = name         
        self._operands  = operands
        self.mgr = mgr 
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

    def __add__(self, other):return self.mgr.newOperator('+',[other,self]) 
    def __sub__(self, other):return self.mgr.newOperator('-',[other,self])    
    def __mul__(self, other):return self.mgr.newOperator('*',[other,self])
    def __pow__(self, other):return self.mgr.newOperator('**',[other,self]) 
    def __truediv__(self, other):return self.mgr.newOperator('/',[other,self]) 
    def __floordiv__(self, other):return self.mgr.newOperator('//',[other,self]) 
    def __mod__(self, other):return self.mgr.newOperator('%',[other,self])

    def __lshift__(self, other):return self.mgr.newOperator('<<',[other,self])
    def __rshift__(self, other):return self.mgr.newOperator('>>',[other,self])
    def __and__(self, other):return self.mgr.newOperator('&',[other,self])
    def __or__(self, other):return self.mgr.newOperator('|',[other,self])
    def __xor__(self, other):return self.mgr.newOperator('^',[other,self])
    def __invert__(self, other):return self.mgr.newOperator('~',[other,self])

    def __lt__(self, other):return self.mgr.newOperator('<',[other,self])
    def __le__(self, other):return self.mgr.newOperator('<=',[other,self])
    def __eq__(self, other):return self.mgr.newOperator('==',[other,self])
    def __ne__(self, other):return self.mgr.newOperator('!=',[other,self])
    def __gt__(self, other):return self.mgr.newOperator('>',[other,self])
    def __ge__(self, other):return self.mgr.newOperator('>=',[other,self])

    def __not__(self):return self.mgr.newOperator('!',[self])
    def __and2__(self, other):return self.mgr.newOperator('&&',[other,self])
    def __or2__(self, other):return self.mgr.newOperator('||',[other,self])

    def __isub__(self, other):return self.mgr.newOperator('-=',[other,self])
    def __iadd__(self, other):return self.mgr.newOperator('+=',[other,self])
    def __imul__(self, other):return self.mgr.newOperator('*=',[other,self])
    def __idiv__(self, other):return self.mgr.newOperator('/=',[other,self])
    def __ifloordiv__(self, other):return self.mgr.newOperator('//=',[other,self])
    def __imod__(self, other):return self.mgr.newOperator('%=',[other,self])
    def __ipow__(self, other):return self.mgr.newOperator('**=',[other,self])


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
        return self.mgr.eval(self,context)
    def vars(self):
        return self.mgr.getVars(self)
    def constants(self):
        return self.mgr.getConstants(self) 
    def operators(self):
        return self.mgr.getOperators(self)
    def functions(self):
        return self.mgr.getFunctions(self)

class Constant(Operand):
    def __init__(self,name,operands=[],mgr=None):
      super(Constant,self).__init__(name,operands,mgr)  
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
    def __init__(self,name,operands=[],mgr=None):
      Operand.__init__(self,name,operands,mgr) 
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
    def __init__(self,name,operands=[],mgr=None):
        super(KeyValue,self).__init__(name,operands,mgr)

    @property
    def value(self): 
        return self._operands[0].value
class Array(Operand):
    def __init__(self,name,operands=[],mgr=None):
      super(Array,self).__init__(name,operands,mgr)

    @property
    def value(self):
        list= []
        for p in self._operands:
            list.append(p.value)
        return list 
class Object(Operand):
    def __init__(self,name,operands=[],mgr=None):
      super(Object,self).__init__(name,operands,mgr)

    @property
    def value(self):
        dic= {}
        for p in self._operands:
            dic[p.name]=p.value
        return dic

class ArrayForeach(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

    @property
    def value(self):
        variable= self._operands[0]
        body= self._operands[1]
        childContext=self.context.newContext()
        self.mgr.setContext(body,childContext)
        for p in variable.value:
            childContext.init(self.name,p)
            body.value
class ArrayMap(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArrayFirst(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArrayLast(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArrayFilter(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArrayReverse(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArraySort(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

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
class ArrayPush(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

    @property
    def value(self):        
        variable= self._operands[0]
        elemnent= self._operands[1]
        value = variable.value
        value.append(elemnent)
        return value
class ArrayPop(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

    @property
    def value(self):        
        variable= self._operands[0]
        index =None
        if len(self._operands)>1:
            index= self._operands[1].value
        else:
            index = len(self._operands) -1        
        return variable.value.pop(index)
class ArrayRemove(Operand,Contextable):
    def __init__(self,name,operands=[],mgr=None):
        Operand.__init__(self,name,operands,mgr)

    @property
    def value(self):        
        variable= self._operands[0]
        element= self._operands[1]
        variable.value.remove(element.value)    

class Function(Operand):
    def __init__(self,name,operands=[],mgr=None):
      Operand.__init__(self,name,operands,mgr)

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
                function=self.mgr.getFunction(name,_type)            
                for p in self._operands:args.append(p.value)
                args.insert(0,value)            
        else:
            function=self.mgr.getFunction(self.name)
            for p in self._operands:args.append(p.value)
        return function(*args)
class Block(Operand):
    def __init__(self,name,elements=[],mgr=None):
      super(Block,self).__init__(name,elements,mgr)

    @property
    def value(self):        
        for p in self._operands:
            p.value

    # TODO
    def debug(self,token:Token,level): 
        pass              
class If(Operand):
    def __init__(self,name,operands=[],mgr=None):
      super(If,self).__init__(name,operands,mgr)      

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
    def __init__(self,name,operands=[],mgr=None):
      super(While,self).__init__(name,operands,mgr)      

    @property
    def value(self): 
        while self.operands[0].value:
           self.operands[1].value

    # TODO
    def debug(self,token:Token,level): 
        pass        

class Operator(Operand):
    def __init__(self,name,operands=[],mgr=None):
      super(Operator,self).__init__(name,operands,mgr)

    @property
    def value(self):
        function = self.mgr.getOperator(self.name,len(self._operands))
        val=self._operands[0].value
        l=len(self._operands)
        i=1
        while i<l:
            val=function(val,self._operands[i].value)
            i+=1
        return val

class UnitaryOperator(Operator):
    @property
    def value(self):
        function = self.mgr.getOperator(self.name,len(self._operands))
        return function(self._operands[0].value)

class BinaryOperator(Operator):
    @property
    def value(self):
        function = self.mgr.getOperator(self.name,len(self._operands))
        return function(self._operands[0].value,self._operands[1].value)

class TernaryOperator(Operator):
    @property
    def value(self):
        function = self.mgr.getOperator(self.name,len(self._operands))
        return function(self._operands[0].value,self._operands[1].value,self._operands[2].value)

class AssigmentOperator(Operator):
    @property
    def value(self):
        if self.name == '=':
            self._operands[0].value = self._operands[1].value
            return self._operands[0].value
        else:
            _oper = self.name.replace('=','')
            function = self.mgr.getOperator(_oper,len(self._operands))
            self._operands[0].value= function(self._operands[0].value,self._operands[1].value)
            return self._operands[0].value       

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
