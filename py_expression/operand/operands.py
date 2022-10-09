from py_expression.model.base import *

class Constant(Operand):
    def __init__(self,name,children=[]):
      super(Constant,self).__init__(name,children)  
      self._type  = type(name).__name__

    @property
    def type(self): 
        return self._type  

    def solve(self,values,token:Token)->Value:
        return Value(self._name)

class Variable(Operand,ContextAble):
    def __init__(self,name:str,children:list[Operand]=[]):
        Operand.__init__(self,name,children)

    def solve(self,values,token:Token)->Value:
        return Value(self.context.get(self._name))

    def set(self,value,token:Token):
        self.context.set(self._name,value)    
    
class KeyValue(Operand):
    def solve(self,values,token:Token)->Value:
        return self._children[0].eval(token)

class Array(Operand):
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value   
                values.append(value.value)
        return Value(values)       

class Object(Operand):
    def solve(self,values,token:Token)->Value:
        
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        dic= {}
        for i,value in enumerate(values):
            dic[self._children[i].name]=value
        return Value(dic)     

class Operator(Operand):
    def __init__(self,name:str,children:list[Operand]=[],function=None):
        super(Operator,self).__init__(name,children) 
        self._function = function
  
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(self._function(*values))                 
                              
class FunctionRef(Operand):
    def __init__(self,name:str,children:list[Operand]=[],function=None):
        super(FunctionRef,self).__init__(name,children) 
        self._function = function

    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(self._function(*values))   

class ArrowFunction(FunctionRef,ChildContextAble):pass

class ContextFunction(FunctionRef):
    def solve(self,values,token:Token)->Value:
        if len(values) == 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value 
            values.append()
        if isinstance(values[0],object) and hasattr(values[0], self._name):
            function=getattr(values[0], self._name)
            for i,p in enumerate(self._children[1:]):
                if i >= len(values):
                    value = p.eval(token)
                    if token.isBreak: return value 
                    values.append(value.value)
            return Value(function(*values[1:]))     
        else:    
            raise Exception('function: '+self._name +' not found in') 

class Block(Operand):
    def solve(self,values,token:Token)->Value:
        for i, p in enumerate(self._children): 
            if i >= len(values):
                value = p.eval(token)
                if token.isBreak: return value     
                values.append(value.value)
        return Value(values)          
                
class If(Operand):
    def solve(self,values,token:Token)->Value:        
        if len(values)== 0:
            # evaluate if condition
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        if len(values)== 1:
            if values[0]:
                # if condition is true evaluate block if
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)                

        # if had elif or else , evaluate them
        if not values[0]:
            index=2
            while len(self._children) > len(values):            
                value = self._children[index].eval(token)
                if token.isBreak: return value
                # en el caso que un elif se haya ejecutado no debe seguir con los posteriores
                if value.value: break
                values.append(value.value)
                index+=1   

        return Value(None)

class ElIf(Operand):
    def solve(self,values,token:Token)->Value:
        if len(values)== 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        if values[0]:
            value = self._children[1].eval(token)
            if token.isBreak: return value
            values.append(value.value) 
                 
        return Value(values[0])

class Else(Operand):
    def solve(self,values,token:Token)->Value:        
        value = self._children[0].eval(token)
        if token.isBreak: return value
        values.append(value.value)
        return Value(True)                 
         
class While(Operand):
    def solve(self,values,token:Token)->Value:
        if len(values)== 0:
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        while values[0]:
            if len(values) < 2:
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)

            values = []
            value = self._children[0].eval(token)
            if token.isBreak: return value
            values.append(value.value)

        return Value(None)   

class For(Operand):
    def solve(self,values,token:Token)->Value:
        pass
    # TODO

class ForIn(Operand):
    def solve(self,values,token:Token)->Value:
        pass
    # TODO
           

  