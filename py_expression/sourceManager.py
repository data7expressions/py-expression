import re
from .base import *
from .coreLib import CoreLib

class SourceManager():
    def __init__(self,model):
        self._model=model
        self._libraries={}

    @property
    def model(self):
        return self._model

    @property
    def libraries(self):
        return self._libraries     

    def addLibrary(self,library):
        self._libraries[library.name] =library

        for name in library.enums:
            self._model.addEnum(name,library.enums[name])

        for name in library.operators:
            operator= library.operators[name]
            for cardinality in operator:
                data = operator[cardinality]
                self._model.addOperator(name,cardinality,data['metadata'])    

        for name in library.functions:
            data = library.functions[name]
            self._model.addFunction(name,data['metadata'])        
  
    def nodeToOperand(self,node:Node)->Operand:
        children = []
        for p in node.children:
            child = self.nodeToOperand(p)
            children.append(child)
        operand = self.createOperand(node.name,node.type,children)
        operand.id = node.id
        return operand

    def reduce(self,operand:Operand,token:Token):
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
                   operand.children[i]=self.reduce(p,token)
        return operand  

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
            raise ExpressionException('set parent: '+operand.name+' error: '+str(error))     

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
            return self.createOperator(name,children)
        elif type == 'functionRef':
            return self.createFunctionRef(name,children)
        elif type == 'arrowFunction':
            return self.createArrowFunction(name,children)
        elif type == 'childFunctionRef':
            if name in self.model.functions:
                return self.createFunctionRef(name,children)
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
            raise ExpressionException('node: '+name +' not supported') 

    def createOperator(self,name:str,children:list[Operand])->Operator:
        try:
            cardinality =len(children)
            metadata = self._model.getOperatorMetadata(name,cardinality)
            if metadata['lib'] in self._libraries:
                implementation= self._libraries[metadata['lib']].operators[name][cardinality]
                if implementation['custom'] is not None:                    
                    return implementation['custom'](name,children,implementation['customFunction']) 
                else:
                    function= implementation['function']
                    return Operator(name,children,function)
            return None
        except Exception as error:
            raise ExpressionException('create operator: '+name+' error: '+str(error))              

    def createFunctionRef(self,name:str,children:list[Operand])->FunctionRef:
        try:            
            metadata = self._model.getFunctionMetadata(name)
            if metadata['lib'] in self._libraries:
                implementation= self._libraries[metadata['lib']].functions[name]
                if implementation['custom'] is not None:                   
                    return implementation['custom'](name,children) 
                else:
                    function= implementation['function']
                    return FunctionRef(name,children,function)
            return None
        except Exception as error:
            raise ExpressionException('cretae function ref: '+name+' error: '+str(error))    
       

    def createArrowFunction(self,name:str,children:list[Operand]):
        try:            
            metadata = self._model.getFunctionMetadata(name)
            if metadata['lib'] in self._libraries:
                implementation= self._libraries[metadata['lib']].functions[name]
                if implementation['custom'] is not None:                    
                    return implementation['custom'](name,children) 
                else:
                    function= implementation['function']
                    return ArrowFunction(name,children,function)
            return None
        except Exception as error:
            raise ExpressionException('create arrow function: '+name+' error: '+str(error))    
        

    

    def setContext(self,operand:Operand,context:Context):
        current = context
        if issubclass(operand.__class__,ChildContextable):
            childContext=current.newContext()
            operand.context = childContext
            current = childContext
        elif issubclass(operand.__class__,Contextable):
            operand.context = current       
        for p in operand.children:
            self.setContext(p,current) 
         
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
            metadata = self._model.getOperatorMetadata(operand.parent.name,len(operand.parent.children))
            if metadata['category'] == 'comparison':
                otherIndex = 1 if operand.index == 0 else 0
                otherOperand= operand.parent.children[otherIndex]
                if isinstance(otherOperand,Constant):
                    return otherOperand.type
                elif isinstance(otherOperand,FunctionRef):    
                    metadata =self.getFunctionMetadata(otherOperand.name)
                    return metadata['return']
                elif isinstance(otherOperand,Operator):    
                    metadata =self._model.getOperatorMetadata(otherOperand.name,len(otherOperand.children))
                    return metadata['return']    
                else:
                    return 'any'
            else:        
                return metadata['args'][operand.index]['type']
        elif isinstance(operand.parent,FunctionRef):
            name = operand.parent.name.replace('.','',1) if operand.parent.name.starWith('.') else  operand.parent.name
            metadata =self._model.getFunctionMetadata(name)
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
    
    def operators(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Operator):
            metadata = self._model.getOperatorMetadata(operand.name,len(operand.children)) 
            list[operand.name] = metadata['category']
        for p in operand.children:
            if isinstance(p,Operator):
                metadata = self._model.getOperatorMetadata(p.name,len(p.children)); 
                list[p.name] =  metadata['category']
            elif len(p.children)>0:
                subList= self.operators(p)
                list = {**list, **subList}
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
            list[key] = self._model.functions[key]
        return list
      
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
        return self.createOperand(serialized['n'],serialized['t'],children)

    def compile(self,node:Node):
        operand =self.nodeToOperand(node)
        operand =self.reduce(operand,Token())
        operand =self.setParent(operand)
        return operand
        
    def eval(self,operand:Operand,context:dict,token:Token)-> Value :  
        if context is not None:
            self.setContext(operand,Context(context))
        try:    
            return operand.eval(token)
        except Exception as error:
            raise ExpressionException('eval: '+Operand.name+' error: '+str(error)) 
  