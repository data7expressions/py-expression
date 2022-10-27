from py_expression.contract.operands import Node, Operand
from py_expression.contract.context import Token
from py_expression.operand.model import Model
from py_expression.operand.helper import helper

class OperandBuilder():
    def __init__(self,model:Model):
        self.__model=model

    def build(self,node:Node)->Operand:
        operand =self.__nodeToOperand(node)
        operand =helper.operand.setParent(operand)
        operand =self.__reduce(operand,Token())
        operand =helper.operand.setParent(operand)
        return operand        
  
    def __nodeToOperand(self,node:Node)->Operand:
        children = []
        if node.children is not None:
            for p in node.children:
                if p is not None:
                    child = self.__nodeToOperand(p)
                    children.append(child)
        operand = self.createOperand(node.name,node.type,children)
        # operand.id = node.id
        return operand

    def __reduce(self,operand:Operand,token:Token)-> Operand:
        """ if all the children are constant, reduce the expression a constant """
        if isinstance(operand,Operator):        
            allConstants=True              
            for p in operand.children:
                if not isinstance(p,Constant):
                    allConstants=False
                    break
            if  allConstants:
                value = operand.eval(token)                
                constant= Constant(value.value)
                constant.parent = operand.parent
                constant.index = operand.index
                return constant
            else:
                for i, p in enumerate(operand.children):
                   operand.children[i]=self.__reduce(p,token)
        return operand  

    def createOperand(self,name:str,type:str,children:list[Operand])->Operand:
        if type == 'constant':
            return Constant(name,children)
        elif type == 'variable':
            return Variable(name,children)
        elif type == 'keyValue':
            return KeyValue(name,children)
        elif type == 'array':
            return Array(name,children)
        elif type == 'object':
            return Object(name,children)
        elif type == 'operator':
            return self.__createOperator(name,children)
        elif type == 'functionRef':
            return self.__createFunctionRef(name,children)
        elif type == 'arrowFunction':
            return self.__createFunctionRef(name,children)
        elif type == 'childFunctionRef':
            if name in self.__model.functions:
                return self.__createFunctionRef(name,children)
            else:
               return ContextFunction(name,children)
        elif type == 'block':
            return  Block(name,children)
        elif type == 'if':
            return  If(name,children)
        elif type == 'elif':
            return  ElIf(name,children)
        elif type == 'else':
            return  Else(name,children)          
        elif type == 'while':
            return  While(name,children)
        elif type == 'for':
            return  For(name,children)
        elif type == 'forIn':
            return  ForIn(name,children)         
        else:
            raise Exception('node: '+name +' not supported') 

    def __createOperator(self,name:str,children:list[Operand])->Operator:
        try:
            cardinality =len(children)
            metadata = self.__model.getOperator(name,cardinality)
            if 'custom' in  metadata and metadata['custom'] is not None:
                if 'chained' in  metadata and metadata['chained'] is not None:                       
                    return metadata['custom'](name,children,metadata['chained'])
                else:
                    return metadata['custom'](name,children) 
            else:                
                return Operator(name,children,metadata['func'])
        except Exception as error:
            raise Exception('create operator: '+name+' error: '+str(error))              

    def __createFunctionRef(self,name:str,children:list[Operand])->FunctionRef:
        try:            
            metadata = self.__model.getFunction(name) 
            if 'custom' in metadata and metadata['custom'] is not None:                   
                return metadata['custom'](name,children) 
            else:
                return FunctionRef(name,children,metadata['func'])
        except Exception as error:
            raise Exception('create function ref: '+name+' error: '+str(error))          
    
  