from py_expression.contract.base import *
from typing import List
from py_expression.operand.coreLibrary import CoreLibrary
from py_expression.operand.model import Model
from py_expression.operand.manager import OperandManager, OperandBuilder
from py_expression.operand.parser import Parser
from py_expression.operand.helper import helper

# Facade  
class Exp(metaclass=Singleton):
    def __init__(self):       
       self.model = Model()
       CoreLibrary(self.model).load() 
    #    self.nodeManager = NodeManager(self.model)
       self.__operand = OperandManager(self.model)

    def addEnum(self,key,source):
        self.model.addEnum(key,source)  

    def build(self,expression:str)->Operand:
        try:               
            minified = helper.node.minify(expression) 
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
        return self.__operand.vars(operand)       

    def operandType(self,operand:Operand)->str:
        return self.__operand.operandType(operand)      

    def constants(self,operand:Operand)->dict:
        return self.__operand.constants(operand)
    
    def operators(self,operand:Operand)->dict:
        return self.__operand.operators(operand)

    def functions(self,operand:Operand)->dict:
        return self.__operand.functions(operand)
        
   
                           