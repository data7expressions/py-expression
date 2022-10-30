from typing import List, Tuple, Any, Union
from lib.contract.base import *
from lib.contract.operands import * 
from lib.contract.context import * 
from lib.contract.managers import IExpressions, ActionObserver
from lib.operand.cache import MemoryCache
from lib.operand.model import ModelManager
from lib.operand.coreLibrary import CoreLibrary
from lib.operand.factory import EvaluatorFactory
from lib.operand.builder import OperandBuilder
from lib.operand.type import TypeManager

# Facade  
class Exp(IExpressions, metaclass=Singleton):
    def __init__(self):       
       self.cache = MemoryCache()
       self.model = ModelManager()
       CoreLibrary(self.model).load()
       self.basic = OperandBuilder(self.model, EvaluatorFactory(self.model))
       self.typeManager = TypeManager(self.model)
       self.observers: List[ActionObserver]=[]
    
    @property
    def enums(self)-> List[Tuple[str, List[Tuple[str, Any]]]]:
        return self.model.enums
    
    @property
    def formats(self)-> List[Tuple[str, Format]]:
        return self.model.formats
    
    @property
    def constants(self)-> List[Tuple[str,Any]]:
        return self.model.constants
    
    @property
    def operators(self)-> List[Tuple[str, OperandMetadata]]:
        return self.model.operators
    
    @property
    def functions(self)-> List[Tuple[str, OperandMetadata]]:
        return self.model.functions
    
    def addEnum (self,name:str, values:Union[List[Tuple[str, Any]], Any]):
        self.model.addEnum(name, values)
    
    def addConstant (self,key:str, value:Any):
        self.model.addConstant(key, value)
        
    def addFormat (self,key:str, pattern:str):
        self.model.addFormat(key, pattern)
        
    def addOperator (self,sing:str,source:Any,priority:int,doc:OperatorDoc=None):
        self.model.addOperator(sing, source, priority,doc)
        
    def addFunction(self,sing:str,source,deterministic:bool=True,doc:OperatorDoc=None):
        self.model.addFunction(sing, source, deterministic,doc)
        
    def addOperatorAlias (self,alias:str, reference:str):
        self.model.addOperatorAlias(alias, reference)
         
    def addFunctionAlias (self,alias:str, reference:str):
        self.model.addFunctionAlias(alias, reference)
        	
    def type (self,expression: str)->Type:
        self.model.addFunctionAlias(expression)
        
    def parameters (self,expression: str)-> List[Parameter]:
        self.model.addFunctionAlias(expression)    
    
    def type (self, expression: str)->str: 
        operand = self.__typed(expression)
        return Type.toString(operand.returnType)
    
    def clone (self,source: Operand)->Operand:
        return self.basic.clone(source)
        
    def eval (self,expression: str, data: Any=None)-> Any:
        context = Context(Data(data))
        operand = self.__basicBuild(expression)
        result = operand.eval(context)
        return result
    
    def run (self,expression: str, data: Any=None)-> Any:
        pass
    
    def subscribe (self,observer:ActionObserver)-> Any:
        self.observers.append(observer)
    
    def unsubscribe (self,observer:ActionObserver)-> Any:
        pass
 
    def __basicBuild (self, expression: str)->Operand:
        try:
            key = hash(expression)
            value = self.cache.get(key)
            if value == None:
                operand = self.basic.build(expression)
                self.cache.set(key, operand)
                return operand
            else:
                return value			
        except Exception as error:
            raise Exception('expression: '+expression+' error: '+str(error)) 
		
    def __typed (self, expression: str)-> Operand:
        key = hash(expression)
        value = self.cache.get(key)
        if value == None:
            operand = self.basic.build(expression)
            self.typeManager.type(operand)
            self.cache.set(key, operand)
            return operand
        elif value.returnType == None:
            self.typeManager.type(value)
            self.cache.set(key, value)
            return value
        else:
            return None