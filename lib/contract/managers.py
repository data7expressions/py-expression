from .type import Type
from .base import *
from .operands import Operand, OperandMetadata, OperatorAdditionalInfo, FunctionAdditionalInfo, OperatorMetadata
from typing import TypeVar, Generic, List, Any, Tuple, Union

class ActionObserverArgs():
    def __init__(self, expression:str, data:Any, result:Any=None, error:Any=None ):
      self.expression = expression
      self.data = data
      self.result = result
      self.error = error

class ActionObserver():
    def __init__(self,condition:str=None):
        self.condition = condition
    def before (self,args:ActionObserverArgs):
        pass
    def after (self,args:ActionObserverArgs):
        pass
    def error (self,args:ActionObserverArgs):
        pass
    
class ITypeManager():
    def type (operand: Operand)->Type:
        pass
    def parameters (operand: Operand)-> List[Parameter]:
        pass

class IModelManager():
    @property
    def enums(self)-> List[Tuple[str, List[Tuple[str, Any]]]]:
        pass
    @property
    def formats(self)-> List[Tuple[str, Format]]:
        pass
    @property
    def constants(self)-> List[Tuple[str,Any]]:
        pass
    @property
    def operators(self)-> List[Tuple[str, OperandMetadata]]:
        pass
    @property
    def functions(self)-> List[Tuple[str, OperandMetadata]]:
        pass
    def addEnum (self,name:str, values: Union[List[Tuple[str, Any]], Any]):
        pass
    def addConstant (self,key:str, value:Any):
        pass
    def addFormat (self,key:str, pattern:str):
        pass
    def addOperator (self,sing:str, source:Any, additionalInfo: OperatorAdditionalInfo):
        pass
    def addFunction(self,sing:str, source:Any, additionalInfo: FunctionAdditionalInfo=None):
        pass
    def addOperatorAlias (self,alias:str, reference:str):
        pass 
    def addFunctionAlias (self,alias:str, reference:str):
        pass    
    def getEnumValue (self,name:str, option:str)-> Any:
        pass
    def getEnum (self,name:str)-> Any:
        pass
    def getFormat (self,name:str)->Format:
        pass
    def getOperator(self,operator:str, operands:int=None)->OperatorMetadata:
        pass
    def getFunction (self,name:str)-> OperatorMetadata:
        pass
    def priority(self,name:str, cardinality:int=None)->int:
        pass	
    def getConstantValue (self,name:str)-> Any:
        pass
    def isEnum (self,name:str)->bool:
        pass
    def isConstant (self,name:str)->bool:
        pass
    def isOperator (self,name:str,operands:int=None)->bool:
        pass
    def isFunction (self,name:str)->bool:
        pass

class IOperandBuilder():
    def build (self,expression: List[str])-> Operand:
        pass
    
    def clone (self, operand: Operand)->Operand:
        pass

class IEvaluatorFactory():
    def create(self,operand:Operand)-> Operand:
        pass

class IExpressions():
    @property
    def enums(self)-> List[Tuple[str, List[Tuple[str, Any]]]]:
        pass
    @property
    def formats(self)-> List[Tuple[str, Format]]:
        pass
    @property
    def constants(self)-> List[Tuple[str,Any]]:
        pass
    @property
    def operators(self)-> List[Tuple[str, OperandMetadata]]:
        pass
    @property
    def functions(self)-> List[Tuple[str, OperandMetadata]]:
        pass
    def addEnum (self,name:str, values:Union[List[Tuple[str, Any]], Any]):
        pass
    def addConstant (self,key:str, value:Any):
        pass
    def addFormat (self,key:str, pattern:str):
        pass
    def addOperator (self,sing:str, source:Any, additionalInfo: OperatorAdditionalInfo):
        pass
    def addFunction(self,sing:str, source:Any, additionalInfo: FunctionAdditionalInfo=None):
        pass
    def addOperatorAlias (self,alias:str, reference:str):
        pass 
    def addFunctionAlias (self,alias:str, reference:str):
        pass	
    def type (self,expression: str)->Type:
        pass
    def parameters (self,expression: str)-> List[Parameter]:
        pass
    def eval (self,expression: str, data: Any=None)-> Any:
        pass
    def run (self,expression: str, data: Any=None)-> Any:
        pass
    def subscribe (self,observer:ActionObserver)-> Any:
        pass
    def unsubscribe (self,observer:ActionObserver)-> Any:
        pass
