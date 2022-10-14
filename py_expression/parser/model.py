from py_expression.model.operands import OperatorType
from py_expression.model.base import Operand
from enum import Enum
import inspect
from typing import List
class Model():
    def __init__(self):
        self._enums={}
        self._constants={}
        self._formats={}
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
            raise Exception('enum not supported: '+key) 

    def addConstant(self,key,source):
        self._constants[key]=source
        
    def addFormat(self,key,source):
        self._formats[key]=source
             
    def addOperatorAlias(self,alias,reference):
        self._operators[alias] = self._operators[reference]
    
    def addFunctionAlias(self,alias,reference):
        self._functions[alias] = self._functions[reference]    
    
    def addOperator(self,sing:str,source,additionalInfo):
        singInfo = self.__getSing(sing)
        name = singInfo['name']
        cardinality = len(singInfo['params'])
        if type(source).__name__ == 'function':
            func = source            
        elif type(source).__name__  == 'type' and issubclass(source, Operand):
            func = source
        else:
            raise Exception('operator ' + singInfo['name'] + 'source not supported')      
        metadata = {            
			'priority': additionalInfo['priority'],
			'deterministic': False,
			'operands': cardinality,			
			'params': singInfo['params'],
			'return': singInfo['return'],
            'func': func
        }
        
        if 'doc' in additionalInfo:
            metadata['doc'] = additionalInfo['doc']
        if 'chainedFunction' in additionalInfo:
            metadata['chainedFunction'] = additionalInfo['chainedFunction']
        if name not in self._operators.keys():
            self._operators[name]= {}           
        self._operators[name][cardinality] = metadata    


    def addFunction(self,sing:str,source,additionalInfo={}):
        singInfo = self.__getSing(sing)
        name = singInfo['name']
        metadata = {            
			'deterministic': additionalInfo['deterministic'] if additionalInfo and additionalInfo['deterministic'] else True,
			'operands': len(singInfo['params']),			
			'params': singInfo['params'],
			'return': singInfo['return']
        }
        if type(source).__name__ == 'function':
            metadata['function'] = source            
        elif type(source).__name__  == 'type' and issubclass(source, Operand):
            metadata['custom'] = source
        else:
            raise Exception('operator ' + singInfo['name'] + 'source not supported') 
        if 'doc' in additionalInfo:
            metadata['doc'] = additionalInfo['doc']
        if 'chainedFunction' in additionalInfo:
            metadata['chainedFunction'] = additionalInfo['chainedFunction']      
        self._functions[name] = metadata   

    def isConstant(self,name):    
        return name in self._constants.keys()
    def getConstantValue(self,name:str):
        return self._constants[name]
    
    def isEnum(self,name):    
        names = name.split('.')
        return names[0] in self.enums.keys()
    def getEnumValue(self,name,option): 
        return self.enums[name][option]
    def getEnum(self,name): 
        return self.enums[name]
    
    def priority(self,name:str,cardinality:int)->int:
        try:
            metadata = self.getOperator(name,cardinality)
            return metadata["priority"] if metadata is not None else -1
        except Exception as error:
            raise Exception('priority: '+name+' error: '+str(error)) 
  
    
    def __getTypeFromValue (self,value:str)->str:
        return value	

    def __getSing(self, sing:str)->dict:
        buffer = list(sing)
        length=len(buffer)
        index = 0
        prefix = ''
        functionName = ''        
        chars:List[str] = []
        
        # Clear begin spaces
        while buffer[index] == ' ' :
            index+=1 
        
        # get function name
        while buffer[index] != '(' :            
            if buffer[index] == ' ' and buffer[index+1] != ' ' and buffer[index+1] != '(':
                prefix = ''.join(chars)
                chars = []
            elif buffer[index] != ' ':
                chars.append(buffer[index])
            index+=1    
        functionName = ''.join(chars)
        
        chars = []
        index+=1        
        params = []
        hadDefault = False
        multiple=False
        name = ''
        _type = ''
        _default= ''        
        while index < length :
            if  buffer[index] == ',' or buffer[index] == ')':
                if hadDefault:
                    _default = ''.join(chars)
                    if _type == '':
                       _type = self.__getTypeFromValue(_default)
                else :
                    _type = ''.join(chars)           
                if name.startswith('...'):
                    multiple = True
                    name = name.replace('...', '')
                # Add Param 
                params.append({'name': name
                             , 'type': _type if _type != '' else 'any'
                             , 'default': _default if _default != '' else None
                             , 'multiple': multiple 
                             
                             })    
                if  buffer[index] == ')':
                    break
                chars = []
                name = ''
                _type = ''
                _default = ''
                hadDefault = False
                multiple = False
            elif buffer[index] == ':':
                name = ''.join(chars)
                chars = []
            elif buffer[index] == '=':
                hadDefault = True
                if name == '':
                    name = ''.join(chars)
                else :
                    _type = ''.join(chars)
                chars = []
            elif buffer[index] != ' ':
                chars.append(buffer[index])
            index+=1    
                        
        chars = []                
        index+=1
        _return = ""
        hadReturn = False
        while index < length :
            if buffer[index] == ':':
                hadReturn = True
            elif buffer[index] != ' ':
                chars.append(buffer[index])
            index+=1
        if hadReturn:
           _return = ''.join(chars)     
        
        return {
            'name': functionName,
            'return': _return if _return != '' else'void',
            'params': params,
            'async': prefix == 'async'
            
        }
    
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
 