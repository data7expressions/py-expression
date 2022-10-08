from .base import *
from typing import List
from ..py_operand.coreLibrary import CoreLib
from ..py_parser.model import Model
from .minifier import *
from ..py_operand.builder import *
from ..py_operand.operand import OperandManager
from ..py_parser.parser import Parser
import py_helper.helper as helper
Helper = helper.Helper

# Facade  
class Exp(metaclass=Singleton):
    def __init__(self):       
       self.model = Model()
       CoreLib(self.model).load() 
    #    self.nodeManager = NodeManager(self.model)
       self.__operand = OperandManager(self.model)

    def addEnum(self,key,source):
        self.model.addEnum(key,source)
  
    # def parse(self,expression:str)->Node:
    #     try:
    #         minified = Helper.node.minify(expression)            
    #         node= self._parse(minified)            
    #         # self.nodeManager.setParent(node)
    #         return node
    #     except Exception as error:
    #         raise Exception('expression: '+expression+' error: '+str(error))
    
    # def _parse(self,buffer:List[str])->Node:                  
    #     _parser = Parser(self.model,buffer)
    #     node= _parser.parse() 
    #     del _parser             
    #     return node

    def build(self,expression:str)->Operand:
        try:               
            minified = Helper.node.minify(expression) 
            return self.__operand.build(minified)
        except Exception as error:
            raise Exception('expression: '+expression+' error: '+str(error))  

    def run(self,expression:str,context:dict={},token:Token=Token())-> any : 
        try:           
            operand = self.build(expression)
            value= self.__operand.eval(operand,context,token)
            return value.value
        except Exception as error:
            raise Exception('expression: '+expression+' error: '+str(error))    

    def serialize(self,operand:Operand)-> dict: 
        return self.__operand.serialize(operand)

    def deserialize(self,serialized:dict,type:str='Operand')->Operand:
        return self.__operand.deserialize(serialized)           
 
    def vars(self,operand:Operand)->dict:
        return self.sourceManager.vars(operand)       

    def operandType(self,operand:Operand)->str:
        return self.sourceManager.operandType(operand)      

    def constants(self,operand:Operand)->dict:
        return self.sourceManager.constants(operand)
    
    def operators(self,operand:Operand)->dict:
        return self.sourceManager.operators(operand)

    def functions(self,operand:Operand)->dict:
        return self.sourceManager.functions(operand)
        
   
                           