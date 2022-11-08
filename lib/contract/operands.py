from enum import Enum
from inspect import Parameter
from pyclbr import Function
from .context import Context
from .type import Type
from .base import Position
from typing import TypeVar, Generic, List, Tuple

class OperandType(Enum):
    Const = 'Const'
    Var = 'Var'
    Env = 'Env'
    Property = 'Property'
    Template = 'Template'
    KeyVal = 'KeyVal'
    List = 'List'
    Obj = 'Obj'
    Operator = 'Operator'
    CallFunc = 'CallFunc'
    Arrow = 'Arrow'
    ChildFunc = 'ChildFunc'
    Block = 'Block'
    If = 'If'
    ElseIf = 'ElseIf'
    Else = 'Else'
    While = 'While'
    For = 'For'
    ForIn = 'ForIn'
    Switch = 'Switch'
    Case = 'Case'
    Default = 'Default'
    Break = 'Break'
    Continue = 'Continue'
    Func = 'Func'
    Return = 'Return'
    Try = 'Try'
    Catch = 'Catch'
    Throw = 'Throw'
    Args = 'Args'

class ParameterDoc():
    def __init__(self, name:str, description:str):
        self.name  = name
        self.description = description  
       
class OperatorDoc():
    def __init__(self, description:str, params:List[ParameterDoc]=[]):
        self.description = description
        self.params = params           

class OperatorInfo():
    def __init__(self, priority:int, doc:OperatorDoc=None):
        self.priority = priority
        self.doc = doc
           
class FunctionInfo():
    def __init__(self, deterministic:bool=True, doc:OperatorDoc=None):
        self.deterministic = deterministic
        self.doc = doc  

class IEvaluator():
    def eval(self, context: Context)->any:
        pass
    
class Operand():
    def __init__(self,pos: Position, name:str, type:OperandType, children:list['Operand']=[], returnType: Type=None):
        self.pos = pos
        self.name  = name
        self.type = type
        self.children = children
        self.returnType = returnType
        self.id  = None
        self.evaluator:IEvaluator = None
        self.number:int = None

    def eval(self,context:Context)->any:
        if self.evaluator is None:
            raise Exception('Evaluator not implemented')
        return self.evaluator.eval(context) 

class Evaluator(IEvaluator):
    def __init__(self,operand:Operand):
        self.operand = operand

class PrototypeEvaluator(IEvaluator):
    def __init__(self,operand:Operand=None):
        self.operand = operand
    def clone(operand: Operand)->IEvaluator:
        pass
    def eval(context: Context)-> any:
        pass

class OperandMetadata():
    def __init__(self, type:OperandType, name:str, children:list['OperandMetadata']=[], returnType: Type=None):
        self.type = type        
        self.name  = name
        self.children = children
        self.returnType = returnType
        self.number:int = None

class OperatorMetadata():
    def __init__(self, params:List[Parameter], deterministic:bool, operands:int, returnType:Type, priority:int=9, function:Function=None, custom:PrototypeEvaluator= None,doc:OperatorDoc=None):
        self.params = params        
        self.deterministic  = deterministic
        self.operands = operands
        self.returnType = returnType
        self.priority = priority
        self.function = function
        self.custom = custom
        self.doc = doc
        