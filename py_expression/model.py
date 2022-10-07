from .base import *

class Model():
    def __init__(self):
        self._enums={}
        self._constants={}
        self._formats={}
        self._aliases={} 
        self._operators={}        
        self._functions={}

    @property
    def enums(self):
        return self._enums
    @property
    def constants(self):
        return self._constants
    @property
    def formats(self):
        return self._formats
    @property
    def aliases(self):
        return self._aliases            
    @property
    def operators(self):
        return self._operators
    @property
    def functions(self):
        return self._functions

    # def addEnum(self,key,source):
    #     self.enums[key]=source

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
            raise Exception('enum not supported: '+key) 

    def addConstant(self,key,source):
        self.constants[key]=source
    def addFormats(self,key,source):
        self.formats[key]=source     
    def addAliases(self,key,source):
        self.aliases[key]=source

    # def addOperator(self,name:str,cardinality:int,metadata):
    #     if name not in self.operators.keys():self.operators[name]= {}    
    #     self.operators[name][cardinality] = metadata  
    def addOperator(self,name:str,category:str,source,priority:int=-1,custom=None,customFunction=None):
        if name not in self._operators.keys():
            self._operators[name]= {}

        metadata = self.getMetadata(source)        
        metadata['priority'] =priority
        metadata['function'] =source
        metadata['custom'] =custom
        metadata['customFunction'] =customFunction
        cardinality = len(metadata['args'])    
        self._operators[name][cardinality] = metadata

    # def addFunction(self:str,name:str,metadata):
    #     self.functions[name] = metadata
    def addFunction(self,name,source,custom=None,isArrowFunction:bool=False):        
        metadata = self.getMetadata(source)
        metadata['function'] =source
        metadata['custom'] =custom        
        metadata['isArrowFunction'] =isArrowFunction        
        self._functions[name] = metadata    

    def isEnum(self,name):    
        names = name.split('.')
        return names[0] in self.enums.keys()
    def getEnumValue(self,name,option): 
        return self.enums[name][option]
    def getEnum(self,name): 
        return self.enums[name]
  
         
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
    

    def getOperator(self,name:str,cardinality:int):
        try:            
            if name in self._operators:
                operator = self._operators[name]
                if cardinality in operator:
                    return operator[cardinality]
            return None        
        except:
            raise Exception('error with operator: '+name)     

    def getFunction(self,name:str):
        try:
            if name in self._functions:
                return self._functions[name]
            return None
        except:
            raise Exception('error with function: '+name)        
 