from lib.contract.base import Sing, Format, Parameter
from lib.contract.operands import OperatorMetadata,OperatorAdditionalInfo, FunctionAdditionalInfo, PrototypeEvaluator 
from lib.contract.managers import IModelManager
from enum import Enum
import inspect
from typing import List, Tuple, Any

class ModelManager(IModelManager):
    def __init__(self):
        self._enums={}
        self._constants={}
        self._formats={}
        self._operators={}        
        self._functions={}
          
    @property
    def constants(self)->List[Tuple[str, Any]]:
        return self._constants.items()
    
    @property
    def formats(self)->List[Tuple[str, Format]]:
        return self._formats.items()
    
    @property
    def enums(self)->List[Tuple[str,List[Tuple[str, Any]]]]:
        return self._enums.items()
                  
    @property
    def operators(self)-> List[Tuple[str, OperatorMetadata]]:
        operators:List[str, OperatorMetadata] = []
        for entry  in self._operators.items():
            for q in entry[1].values():
                operators.append([entry[0], q])
        return operators
        
    @property
    def functions(self)-> List[Tuple[str, OperatorMetadata]]:
        return self._functions.items()

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
    
    def addOperator(self,sing:str,source:Any,additionalInfo:OperatorAdditionalInfo):
        singInfo = self.__getSing(sing)
        metadata = {            
			'priority': additionalInfo.priority,
			'deterministic': False,
			'operands': len(singInfo.params),			
			'params': singInfo.params,
			'returnType': singInfo.returnType
        }
        if issubclass(source,PrototypeEvaluator):
            metadata['custom'] = source
        if type(source).__name__ == 'function':
            metadata['func'] = source            
        else:
            raise Exception('Operator ' + singInfo.name + 'source not supported')          
        if 'doc' in additionalInfo:
            metadata['doc'] = additionalInfo.doc
        if singInfo.name not in self._operators.keys():
            self._operators[singInfo.name]= {}           
        self._operators[singInfo.name][metadata.operands] = metadata

    def addFunction(self,sing:str,source,additionalInfo:FunctionAdditionalInfo=None):
        singInfo = self.__getSing(sing)
        metadata = {            
			'deterministic': additionalInfo['deterministic'] if additionalInfo and additionalInfo['deterministic'] else True,
			'operands': len(singInfo.params),			
			'params': singInfo.params,
			'returnType': singInfo.returnType
        }
        if issubclass(source,PrototypeEvaluator):
            metadata['custom'] = source
        if type(source).__name__ == 'function':
            metadata['func'] = source            
        else:
            raise Exception('Function ' + singInfo.name + 'source not supported')   
        if 'doc' in additionalInfo:
            metadata['doc'] = additionalInfo.doc
        self._functions[singInfo.name] = metadata
    
    def getConstantValue(self,name:str)->Any:
        return self._constants[name]     
    
    def getEnumValue(self,name,option)->Any: 
        return self.enums[name][option]
    
    def getEnum(self,name)->List[Tuple[str,Any]]: 
        return self.enums[name]
    
    def getOperator(self,name:str,cardinality:int)->OperatorMetadata:
        try:            
            if name in self._operators:
                operator = self._operators[name]
                if cardinality in operator:
                    return operator[cardinality]
            return None        
        except:
            raise Exception('error with operator: '+name)     

    def getFunction(self,name:str)->OperatorMetadata:
        try:
            if name in self._functions:
                return self._functions[name]
            return None
        except:
            raise Exception('error with function: '+name)   
    
    def isConstant(self,name:str)->bool:    
        return name in self._constants.keys()
    
    def isEnum(self,name:str)->bool:      
        names = name.split('.')
        return names[0] in self.enums.keys()
    
    def isOperator (self, name:str, operands:int=None)->bool:
        operators = self._operators[name]
        if operands != None:
            return operators and operators[operands] != None
        return operators != None
    
    def isFunction (self,name:str)->bool:
        return self._functions[name] != None	
    
    def priority(self,name:str,cardinality:int)->int:
        try:
            metadata = self.getOperator(name,cardinality)
            return metadata["priority"] if metadata is not None else -1
        except Exception as error:
            raise Exception('priority: '+name+' error: '+str(error))   
    
    def __getTypeFromValue (self,value:str)->str:
        return value	

    def __getSing(self, sing:str)->Sing:
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
                             , 'type': _type if _type != '' else 'Any'
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
                   
        return Sing(functionName,- params, _return if _return != '' else 'void', prefix == 'async')        
    
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
        if(_type == '<built-in function Any>'):return 'Any'
        elif (_type == 'inspect._empty'):return None
        return _type
 