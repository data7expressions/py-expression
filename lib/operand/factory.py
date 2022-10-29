from lib.contract.base import *
from lib.contract.operands import *
from lib.contract.type import *
from lib.contract.managers import *
from lib.operand.helper import helper
from typing import List, Tuple
from .evaluators import *

class ConstBuilder():
	def build (pos:Tuple[int, int], value:any)->Operand:
		operand = Operand(pos, value, OperandType.Const, [], Type.get(value))
		operand.evaluator = ConstEvaluator(operand)
		return operand

class EvaluatorFactory(IEvaluatorFactory):    
    def __init__(self, model: IModelManager):
        self.model = model

    def createOperator (self, operand:Operand)->IEvaluator:
        operatorMetadata = self.model.getOperator(operand.name, operand.children.length)
        if operatorMetadata.custom != None:
            return operatorMetadata.custom.clone(operand)
        elif operatorMetadata.function != None:
            return CallFuncEvaluator(operand, operatorMetadata.function)
        else:
            raise Exception('Operator '+ operand.name +' not implemented')	

    def createFunction (self, operand:Operand)->IEvaluator:
        operatorMetadata = self.model.getOperator(operand.name, operand.children.length)
        if operatorMetadata.custom != None:
            return operatorMetadata.custom.clone(operand)
        elif operatorMetadata.function != None:
            return CallFuncEvaluator(operand, operatorMetadata.function)
        else:
            raise Exception('Function '+ operand.name +' not implemented')

    def create (self,operand:Operand)->IEvaluator:
        evaluator= None		
        if operand.type == OperandType.Const:
            evaluator = ConstEvaluator(operand)
        elif operand.type == OperandType.Var:
            evaluator = VarEvaluator(operand)   
        elif operand.type == OperandType.Env:
            evaluator = EnvEvaluator(operand)
        elif operand.type == OperandType.Template:
            evaluator = TemplateEvaluator(operand)
        elif operand.type == OperandType.Property:
            evaluator = PropertyEvaluator(operand)
        elif operand.type == OperandType.List:
            evaluator = ListEvaluator(operand)
        elif operand.type == OperandType.Obj:
            evaluator = ObjEvaluator(operand)
        elif operand.type == OperandType.Operator:
            evaluator = self.createOperator(operand)
        elif operand.type in [OperandType.CallFunc,OperandType.Arrow,OperandType.ChildFunc]:
            evaluator = self.createFunction(operand)
        elif operand.type == OperandType.Block:
            evaluator = BlockEvaluator(operand)
        elif operand.type == OperandType.If:
            evaluator = IfEvaluator(operand)
        elif operand.type == OperandType.While:
            evaluator = WhileEvaluator(operand)
        elif operand.type == OperandType.For:
            evaluator = ForEvaluator(operand)
        elif operand.type == OperandType.ForIn:
            evaluator = ForInEvaluator(operand)
        elif operand.type == OperandType.Switch:
            evaluator = SwitchEvaluator(operand)
        elif operand.type == OperandType.Break:
            evaluator = BreakEvaluator(operand)
        elif operand.type == OperandType.Continue:
            evaluator = ContinueEvaluator(operand)
        elif operand.type == OperandType.Func:
            evaluator = FuncEvaluator(operand)
        elif operand.type == OperandType.Return:
            evaluator = ReturnEvaluator(operand)
        elif operand.type == OperandType.Try:
            evaluator = TryEvaluator(operand)
        elif operand.type == OperandType.Catch:
            evaluator = CatchEvaluator(operand)
        elif operand.type == OperandType.Throw:
            evaluator = ThrowEvaluator(operand)
        elif operand.type in [OperandType.Default,OperandType.Case,OperandType.KeyVal,OperandType.ElseIf,OperandType.Else]:
            evaluator=None
        else:
            raise Exception('Evaluator for '+operand.type+ ' ' + operand.name+ ' not found')		
        return evaluator
