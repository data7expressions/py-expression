from py_expression.contract.operands import *
from py_expression.contract.context import Token
from py_expression.contract.managers import *
from py_expression.operand.helper import helper
from .factory import ConstBuilder
from .parser import Parser

class OperandBuilder():
    def __init__(self,model:IModelManager,factory: IEvaluatorFactory):
        self.model=model
        self.factory=factory

    def build (self, expression: str)-> Operand:
        operand = Parser(self.model, expression).parse()
        self.complete(operand, 1)
        reduced = self.reduce(operand)
        return reduced

    def reduce (self,operand: Operand)->Operand:
        if operand.type == OperandType.Operator:
            return self.reduceOperand(operand)
        elif operand.type == OperandType.CallFunc:
			#  Example: .[0].states.filter() where function name is states.filter
            names = operand.name.split('.')
            funcName = names[names.length - 1]
            funcMetadata = self.model.getFunction(funcName)
            if funcMetadata != None and funcMetadata.deterministic:
                return self.reduceOperand(operand)
        return operand

    def reduceOperand (self, operand: Operand)->Operand: 
        allConstants = True
        for child in operand.children:
            if not (child.type == OperandType.Const):
                allConstants = False
                break
        if allConstants:
            value = operand.eval(Context())
            constant = ConstBuilder().build(operand.pos, value)
            constant.id = operand.id
            return constant
        else:
            i = 0
            while i < len(operand.children):
                child = operand.children[i]
                operand.children[i] = self.reduce(child)
                i+=1
        return operand
    
    def complete (self, operand: Operand, index:int, parentId:str=None):
        id = parentId if parentId + '.' + index else str(index)
        if operand.children != None:
            for i, child in enumerate(operand.children):				
                self.complete(child, i + 1, id)
        operand.id = id
        operand.evaluator = self.factory.create(operand)
  