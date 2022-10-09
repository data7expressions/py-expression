from py_expression.model import *
from py_expression.core.context import *
from py_expression.operand.operands import *
from .builder import OperandBuilder
from .serializer import OperandSerializer
from py_expression.parser.parser import Parser, Model
from typing import List

class OperandManager():
    def __init__(self,model:Model):
        self.__model=model
        self.__builder=OperandBuilder(self.__model) 
        self.__serializer=OperandSerializer(self.__builder)
        
    def serialize(self,operand:Operand)-> dict:
        return self.__serializer.serialize(operand)

    def deserialize(self,serialized:dict)-> Operand:
        return self.__serializer.deserialize(serialized)              
       
    def build(self,buffer:List[str])->Operand:                  
        _parser = Parser(self.__model,buffer)
        node= _parser.parse() 
        del _parser
        return self.__builder.build(node)
    
    def eval(self,operand:Operand,context:dict,token:Token)-> Value :  
        if context is not None:
            self.__setContext(operand,Context(context))
        try:    
            return operand.eval(token)
        except Exception as error:
            raise Exception('eval: '+Operand.name+' error: '+str(error)) 
             
    def vars(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Variable):
            list[operand.name] = self.operandType(operand)
        for p in operand.children:
            if isinstance(p,Variable):
                list[p.name] = self.operandType(p)
            elif len(p.children)>0:
                subList= self.vars(p)
                list = {**list, **subList}
        return list 

    def operandType(self,operand:Operand)->str:
        """ """
        if isinstance(operand.parent,Operator):
            metadata = self.__model.getOperator(operand.parent.name,len(operand.parent.children))
            # if metadata['category'] == 'comparison':
            #     otherIndex = 1 if operand.index == 0 else 0
            #     otherOperand= operand.parent.children[otherIndex]
            #     if isinstance(otherOperand,Constant):
            #         return otherOperand.type
            #     elif isinstance(otherOperand,FunctionRef):    
            #         metadata =self.getFunctionMetadata(otherOperand.name)
            #         return metadata['return']
            #     elif isinstance(otherOperand,Operator):    
            #         metadata =self.__model.getOperatorMetadata(otherOperand.name,len(otherOperand.children))
            #         return metadata['return']    
            #     else:
            #         return 'any'
            # else:        
            return metadata['args'][operand.index]['type']
        elif isinstance(operand.parent,FunctionRef):
            name = operand.parent.name.replace('.','',1) if operand.parent.name.starWith('.') else  operand.parent.name
            metadata =self.__model.getFunction(name)
            return metadata['args'][operand.index]['type'] 

    def constants(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Constant):
            list[operand.name] = operand.type
        for p in operand.children:
            if isinstance(p,Constant):
                list[p.name] = p.type
            elif len(p.children)>0:
                subList= self.constants(p)
                list = {**list, **subList}
        return list
    
    def operators(self,operand:Operand)->Array:
      list = []
      if isinstance(operand,Operator):	
        list.append(operand.name)
      for p in operand.children:
        list = list + self.operators(p)
      return list 
      
    def functions(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,FunctionRef):
            list[operand.name] = {}
        for p in operand.children:
            if isinstance(p,FunctionRef):
                list[p.name] = {}
            elif len(p.children)>0:
                subList= self.functions(p)
                list = {**list, **subList}

        for key in list:
            list[key] = self.__model.functions[key]
        return list
    
    def __setContext(self,operand:Operand,context:Context):
        current = context
        if issubclass(operand.__class__,ChildContextAble):
            childContext=current.newContext()
            operand.context = childContext
            current = childContext
        elif issubclass(operand.__class__,ContextAble):
            operand.context = current       
        for p in operand.children:
            self.__setContext(p,current) 
    
    def clone (self,operand: Operand)-> Operand:
	    return self.__serializer.clone(operand) 