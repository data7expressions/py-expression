import re
from .base import *
from .coreLib import CoreLib

class NodeManager():
    def __init__(self,model):
       self._model = model    
          
    def vars(self,node:Node):
        list = {}
        if node.type == 'variable':
            list[node.name] = self.operandType(node)
        for p in node.children:
            if p.type =='variable':
                list[p.name] = self.operandType(p)
            elif len(p.children)>0:
                subList= self.vars(p)
                list = {**list, **subList}
        return list 

    def operandType(self,node:Node)->str:
        """ """
        if node.parent.type == 'operator':
            metadata = self._model.getOperator(node.parent.name,len(node.parent.children))
            # if metadata['category'] == 'comparison':
            #     otherIndex = 1 if node.index == 0 else 0
            #     otherOperand= node.parent.children[otherIndex]
            #     if otherOperand.type == 'constant':
            #         return type(otherOperand.name).__name__ 
            #     elif otherOperand.type == 'functionRef':    
            #         metadata =self._model.getFunction(otherOperand.name)
            #         return metadata['return']
            #     elif otherOperand.type == 'operator':    
            #         metadata =self._model.getOperator(otherOperand.name,len(otherOperand.children))
            #         return metadata['return']    
            #     else:
            #         return 'any'
            # else:        
            return metadata['args'][node.index]['type']
        elif node.parent.type == 'functionRef':            
            metadata =self._model.getFunctionMetadata(node.parent.name)
            return metadata['args'][node.index]['type'] 

    def constants(self,node:Node)->dict:
        list = {}
        if node.type == 'constant':
            list[node.name] = type(node.name).__name__ 
        else:    
            for p in node.children:
                if p.type == 'constant':
                    list[p.name] = type(p.name).__name__ 
                elif len(p.children)>0:
                    subList= self.constants(p)
                    list = {**list, **subList}
        return list

    def functions(self,node:Node)->dict:
        list = {}
        if node.type == 'functionRef':
            list[node.name] = {}
        for p in node.children:
            if p.type == 'functionRef':
                list[p.name] = {}
            elif len(p.children)>0:
                subList= self.functions(p)
                list = {**list, **subList}

        for key in list:
            list[key] = self._model.functions[key]
        return list
      
    def operators(self,node:Node)->Array:
      list = []
      if node.type == 'operator':	
        list.append(node.name)
      for p in node.children:
        list = list + self.operators(p)
      return list  

    def serialize(self,node:Node)-> dict:
        children = []                
        for p in node.children:
            children.append(self.serialize(p))
        return {'id':node.id,'n':node.name,'t':node.type,'c':children} 

    def deserialize(self,serialized:dict)-> Node:
        node = self._deserialize(serialized)
        node =self.setParent(node)
        return node

    def _deserialize(self,serialized:dict)-> Node:
        children = []
        if 'c' in serialized:
            for p in serialized['c']:
                children.append(self._deserialize(p))
        return  Node(serialized['n'],serialized['t'],children)

    def setParent(self,node:Node,parent:Node=None,index:int=0):
        try:
            if parent is not None:
                node.id = parent.id +'.'+str(index)
                node.parent = parent
                node.index = index
                node.level = parent.level +1  
            else:
                node.id = '0'
                node.parent = None
                node.index = 0
                node.level = 0 

            if  node.children and len(node.children)>0:
                for i,p in enumerate(node.children):
                    if p is not None:
                        self.setParent(p,node,i) 
        except Exception as error:
            raise Exception('set parent: '+node.name+' error: '+str(error)) 
       
        return node;              
