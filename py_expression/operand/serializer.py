from py_expression.model.base import *
from .builder import OperandBuilder

class OperandSerializer():
    def __init__(self,builder:OperandBuilder):
        self.builder=builder
    
    def serialize(self,operand:Operand)-> dict:
        children = []                
        for p in operand.children:
            children.append(self.serialize(p))
        return {'id': operand.id, 'n':operand.name,'t':type(operand).__name__,'c':children} 

    def deserialize(self,serialized:dict)-> Operand:
        operand = self._deserialize(serialized)
        operand =self.setParent(operand)
        return operand

    def _deserialize(self,serialized:dict)-> Operand:
        children = []
        if 'c' in serialized:
            for p in serialized['c']:
                children.append(self._deserialize(p))
        return self.builder.createOperand(serialized['n'],serialized['t'],children)
    
    def clone (self,operand: Operand)-> Operand:
	    return self.deserialize(self.serialize(operand))