import re
from typing import List
from py_expression.model.base import *

class ValidatorHelper():
    def __init__(self):
        self._reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$')
        self._reInt = re.compile('[0-9]+$')
        self._reDecimal = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')        
        
    def isAlphanumeric(self,value:str)->bool:
        return self._reAlphanumeric.match(value)
    def isIntegerFormat(self,value:str)->bool:
        return self._reInt.match(value)
    def isDecimalFormat(self,value:str)->bool:
        return self._reDecimal.match(value)
    
    
    
    
class NodeHelper():
    def __init__(self,validator:ValidatorHelper):
        self.validator = validator

    def minify(self,expression)->List[str]:
        isString=False
        quotes=None
        buffer = list(expression)
        length=len(buffer)
        result =[]
        i=0
        while i < length:
            p =buffer[i]        
            if isString and p == quotes: isString=False 
            elif not isString and (p == '\'' or p=='"'):
                isString=True
                quotes=p
            if isString:
                result.append(p)
            elif  p == ' ' :
                # solo debería dejar los espacios cuando es entre caracteres alfanuméricos. 
                # por ejemplo en el caso de "} if" no debería quedar un espacio 
                if i+1 < length and self.validator.isAlphanumeric(buffer[i-1]) and self.validator.isAlphanumeric(buffer[i+1]):
                    result.append(p)                
            elif (p!='\n' and p!='\r' and p!='\t' ):
               result.append(p)
            i+=1   
        return result
    
    def serialize(self,node:Node)-> dict:
        children = []                
        for p in node.children:
            children.append(self.serialize(p))
        return {'n':node.name,'t':node.type,'c':children} 

    def deserialize(self,serialized:dict)-> Node:
        children = []
        if 'c' in serialized:
            for p in serialized['c']:
                children.append(self.deserialize(p))
        return  Node(serialized['n'],serialized['t'],children)

class OperandHelper():
    
    def setParent(self,operand:Operand,index:int=0,parent:Operand=None):        
        try:
            if parent is not None:
                operand.id = parent.id +'.'+str(index)
                operand.parent = parent
                operand.index = index
                operand.level = parent.level +1  
            else:
                operand.id = '0'
                operand.parent = None
                operand.index = 0
                operand.level = 0 
            
            for i,p in enumerate(operand.children):
                self.setParent(p,i,operand)           
            return operand
        except Exception as error:
            raise Exception('set parent: '+operand.name+' error: '+str(error)) 

class ExpHelper():
    def __init__(self):
        self._validator = ValidatorHelper()
        self._node = NodeHelper(self._validator )
        self._operand = OperandHelper()        
        
    @property
    def validator(self):
        return self._validator
    
    @property
    def node(self):
        return self._node  
    
    @property
    def operand(self):
        return self._operand  

Helper = ExpHelper()