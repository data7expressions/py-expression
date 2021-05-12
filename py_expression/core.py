from .base import *
from .coreLib import CoreLib
from .minifier import *
from .sourceManager import *
from .nodeManager import *
from .parser import Parser

# Facade  
class Exp(metaclass=Singleton):
    def __init__(self):
       self.model = Model()
       self.minifier = Minifier()
       self.parser = Parser(self.model)
       self.nodeManager = NodeManager(self.model)
       self.sourceManager = SourceManager(self.model)        
       self.addLibrary(CoreLib())        

    def addLibrary(self,library):
        self.sourceManager.addLibrary(library)
        self.refresh() 
    
    def refresh(self):
        self.parser.refresh()    
    
    def minify(self,expression:str)->list[str]:
        return self.minifier.minify(expression) 
  
    def parse(self,expression:str)->Node:
        try:
            minified = self.minify(expression) 
            node= self.parser.parse(minified)            
            self.nodeManager.setParent(node)
            return node
        except Exception as error:
            raise ExpressionException('expression: '+expression+' error: '+str(error))

    def compile(self,expression)->Operand:
        try:
            node=None
            if isinstance(expression,Node):
                node=expression                
            elif isinstance(expression,str):
                node = self.parse(expression)
            else:
               raise ExpressionException('not possible to compile')      

            return self.sourceManager.compile(node)
        except Exception as error:
            raise ExpressionException('node: '+node.name+' error: '+str(error))  

    def run(self,expression,context:dict={},token:Token=Token())-> any : 
        try:
            operand=None
            if isinstance(expression,Operand):
                operand=expression
            elif isinstance(expression,Node):                
                operand =self.sourceManager.compile(expression)                   
            elif isinstance(expression,str):
                node = self.parse(expression)
                operand =self.sourceManager.compile(node) 
            else:
               raise ExpressionException('not possible to run')  

            value= self.sourceManager.eval(operand,context,token)
            return value.value
        except Exception as error:
            raise ExpressionException('operand: '+operand.name+' error: '+str(error))    

    def serialize(self,value)-> dict:        
        if isinstance(value,Node):
            return self.nodeManager.serialize(value)
        elif isinstance(value,Operand):
            return self.sourceManager.serialize(value)
        return None      

    def deserialize(self,serialized:dict,type:str='Operand'):
        if type == 'Operand':
            return self.sourceManager.deserialize(serialized)
        elif type == 'Node':
            return self.nodeManager.deserialize(serialized)
        else:
            raise ExpressionException('type: '+type+' not support')           
 
    def vars(self,value)->dict:
        if isinstance(value,Node):
            return self.nodeManager.vars(value)
        elif isinstance(value,Operand):
            return self.sourceManager.vars(value)
        return None       

    def operandType(self,value)->str:
        if isinstance(value,Node):
            return self.nodeManager.operandType(value)
        elif isinstance(value,Operand):
            return self.sourceManager.operandType(value) 
        return None     

    def constants(self,value)->dict:
        if isinstance(value,Node):
            return self.nodeManager.constants(value)
        elif isinstance(value,Operand):
            return self.sourceManager.constants(value)
        return None 
    
    def operators(self,value)->dict:
        if isinstance(value,Node):
            return self.nodeManager.operators(value)
        elif isinstance(value,Operand):
            return self.sourceManager.operators(value)
        return None

    def functions(self,value)->dict:
        if isinstance(value,Node):
            return self.nodeManager.functions(value)
        elif isinstance(value,Operand):
            return self.sourceManager.functions(value)
        return None
        
   
                           