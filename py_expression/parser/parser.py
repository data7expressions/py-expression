from typing import List
from py_expression.model.base import *
from .model import Model
import py_expression.helper.helper as helper
Helper = helper.Helper

class Parser():
    def __init__(self,model:Model,buffer:List[str]):
       self.model = model       
       self.buffer = buffer
       self.length=len(self.buffer)
       self.index=0
       self.tripleOperators = []
       self.doubleOperators = [] 
       self.assignmentOperators = []
       self.arrowFunction = []
       self.setOperators()
    
    def setOperators(self):
        for key in self.model.operators.keys():
            if len(key)==2: 
                self.doubleOperators.append(key)
            elif len(key)==3: 
                self.tripleOperators.append(key)

            operator = self.model.operators[key]
            if 2 in operator.keys():
            #    if operator[2]['category'] == 'assignment':
               if operator[2]['priority'] == 1: 
                  self.assignmentOperators.append(key)

        # for key in self.model.functions.keys():
        #     metadata = self.model.functions[key]
        #     if metadata['isArrowFunction']: 
        #         self.arrowFunction.append(key)   
    
    def parse(self)->Node:
        nodes=[]
        while not self.end:
            node =self.getExpression(_break=';')
            if node is None:break
            nodes.append(node)
        if len(nodes)==1 :
            return nodes[0]
        return Node('block','block',nodes)

    @property
    def previous(self):
        return self.buffer[self.index-1] 
    @property
    def current(self):
        return self.buffer[self.index]    
    @property
    def next(self):
        return self.buffer[self.index+1]
    @property
    def end(self):
        return self.index >= self.length 

    def nextIs(self,key):
        arr = list(key)        
        for i, p in enumerate(arr):
            if self.buffer[self.index+i] != p:
                return False
        return True         

    def getExpression(self,operand1=None,operator=None,_break='')->Node:
        expression = None
        operand2 = None
        isBreak = False               
        while not self.end:
            if operand1 is None and operator is None: 
                operand1=  self.getOperand()
                operator= self.getOperator()
                if operator is None or operator == ' ' or operator in _break: 
                    expression = operand1
                    isBreak= True
                    break
            operand2=  self.getOperand()
            nextOperator= self.getOperator()
            if nextOperator is None or nextOperator in _break:
                expression= Node(operator,'operator',[operand1,operand2])
                isBreak= True
                break
            elif self.priority(operator)>=self.priority(nextOperator):
                operand1=Node(operator,'operator',[operand1,operand2])
                operator=nextOperator
            else:
                operand2 = self.getExpression(operand1=operand2,operator=nextOperator,_break=_break)
                expression= Node(operator,'operator',[operand1,operand2])
                isBreak= True
                break
        if not isBreak: expression=Node(operator,'operator',[operand1,operand2])
        return expression  

    def getOperand(self)-> Node:        
        isNegative=False
        isNot=False
        isBitNot=False
        operand=None
        while self.current == ' ' and not self.end: self.index+=1
        if self.end: return None
        char = self.current
        if char == '-':
           isNegative=True
           self.index+=1
           char = self.current
        elif char == '~':
           isBitNot=True
           self.index+=1
           char = self.current            
        elif char == '!':
           isNot=True
           self.index+=1
           char = self.current   

        if char.isalnum():    
            value=  self.getValue()
            if value=='function' and self.current == ' ': 
                self.index+=1
                operand = self.getFunction()
            elif value=='if' and self.current == '(': 
                self.index+=1
                operand = self.getIfBlock()
            elif value=='for' and self.current == '(': 
                self.index+=1
                operand = self.getForBlock()    
            elif value=='while' and self.current == '(': 
                self.index+=1
                operand = self.getWhileBlock()   
            elif value=='switch' and self.current == '(': 
                self.index+=1
                operand = self.getSwitchBlock()
            elif not self.end and self.current == '(':
                self.index+=1
                if '.' in value:
                    names = value.split('.')
                    name = names.pop()
                    variableName= '.'.join(names)
                    variable = Node(variableName,'variable')
                    operand= self.getChildFunction(name,variable)
                else:
                    args=  self.getArgs(end=')')
                    operand= Node(value,'functionRef',args)                

            elif value=='try' and self.current == '{':
                operand = self.getTryCatchBlock()
            elif not self.end and self.current == '[':
                self.index+=1    
                operand = self.getIndexOperand(value) 
            elif value=='throw':   
                operand = self.getThrow()
            elif value=='return':   
                operand = self.getReturn()    
            elif value=='break':                
                operand = Node('break','break')
            elif value=='continue':                
                operand = Node('continue','continue')
            elif self.model.isConstant(value):
                constantValue = self.model.getConstantValue(value)                
                operand = Node(constantValue,'constant')
            elif Helper.validator.isIntegerFormat(value): 
                if isNegative:
                    value = int(value)* -1
                    isNegative= False 
                elif isBitNot:
                    value = ~ int(value)
                    isBitNot= False     
                else:
                    value =int(value)
                operand = Node(value,'constant')
            elif Helper.validator.isDecimalFormat(value):
                if isNegative:
                    value = float(value)* -1
                    isNegative= False
                elif isBitNot:
                    value = ~float(value)
                    isBitNot= False      
                else:
                    value =float(value)
                operand = Node(value,'constant')            
            elif self.model.isEnum(value):                
                operand= self.getEnum(value)
            else:
                operand = Node(value,'variable')
        elif char == '\'' or char == '"':
            self.index+=1
            result=  self.getString(char)
            operand= Node(result,'constant')
        elif char == '(':
            self.index+=1
            operand=  self.getExpression(_break=')') 
        elif char == '{':
            self.index+=1
            operand = self.getObject()  
        elif char == '[':
            self.index+=1
            elements=  self.getArgs(end=']')
            operand =  Node('array','array',elements)        

        operand = self.solveChain(operand)

        if isNegative:operand= Node('-','operator',[operand])
        if isNot:operand=Node('!','operator',[operand])
        if isBitNot:operand=Node('~','operator',[operand])  
        return operand

    def solveChain(self,operand):
        if not self.end and  self.current=='.':
            self.index+=1
            name=  self.getValue()
            if self.current == '(': self.index+=1
            return self.solveChain(self.getChildFunction(name,operand))
        else:    
            return  operand        

    def priority(self,op:str,cardinality:int=2)->int:
        return self.model.priority(op,cardinality)        

    def getValue(self,increment:bool=True):
        buff=[]
        if increment:
            while not self.end and Helper.validator.isAlphanumeric(self.current):
                buff.append(self.current)
                self.index+=1            
        else:
            index = self.index
            while not self.end and Helper.validator.isAlphanumeric(self.buffer[index]):
                buff.append(self.buffer[index])
                index+=1        
        return ''.join(buff)

    def getOperator(self):
        if self.end:return None
        op=None
        if self.index+2 < self.length:
            triple = self.current+self.next+self.buffer[self.index+2]
            if triple in self.tripleOperators :op=triple
        if op is None and  self.index+1 < self.length:
            double = self.current+self.next
            if double in self.doubleOperators  :op=double
        if op is None:op=self.current 
        self.index+=len(op)
        return op

    def getString(self,char):
        buff=[]       
        while not self.end :
            if self.current == char:
                if not((self.index+1 < self.length and self.next == char) or (self.previous == char)):
                    break 
            buff.append(self.current)
            self.index+=1
        self.index+=1    
        return ''.join(buff)

    def getArgs(self,end=')'):
        args= []
        while True:
            arg= self.getExpression(_break=','+end)
            if arg is not None:args.append(arg)
            if self.previous==end: break
        return args

    def getObject(self):
        attributes= []
        while True:
            name=None
            if self.current== '"' or  self.current == "'":
                char= self.current
                self.index+=1
                name= self.getString(char)
            else:    
                name= self.getValue()
            if self.current==':':self.index+=1
            else:raise Exception('attribute '+name+' without value')
            value= self.getExpression(_break=',}')
            attribute = Node(name,'keyValue',[value])
            attributes.append(attribute)
            if self.previous=='}':
                break
        
        return  Node('object','object',attributes) 

    def getBlock(self):
        lines= []
        while True:
            line= self.getExpression(_break=';}')
            if line is not None :lines.append(line)
            if self.previous=='}':
                break        
        return Node('block','block',lines) 

    def getControlBlock(self):
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';')
        return block            

    def getIfBlock(self):
        children = []
        condition= self.getExpression(_break=')')
        children.append(condition)
        block = self.getControlBlock()
        children.append(block)

        while self.nextIs('else if('):
            self.index+=len('else if(')
            condition= self.getExpression(_break=')')
            block = self.getControlBlock()
            elifNode = Node('elif','elif',[condition,block])
            children.append(elifNode)

        if self.nextIs('else'):
            self.index+=len('else')
            block = self.getControlBlock()
            elseNode = Node('else','else',[block])            
            children.append(elseNode)     
        
        return Node('if','if',children)   
        
    def getSwitchBlock(self):
        
        value= self.getExpression(_break=')')
        if self.current == '{': self.index+=1          

        if self.nextIs('case'):next='case'
        elif self.nextIs('default:'):next='default:'

        children = []
        while next=='case':
            self.index+=len('case')
            if self.current == '\'' or self.current == '"':
                char = self.current
                self.index+=1
                compare=  self.getString(char)
            else:    
                compare= self.getValue()

            if self.current == ':':self.index+=1
            lines=[]
            while True:
                line= self.getExpression(_break=';')
                if line is not None :lines.append(line)
                if self.nextIs('case'):
                    next='case'
                    break
                elif self.nextIs('default:'): 
                    next = 'default:'
                    break
                elif self.current == '}':
                    next = 'end'
                    break

            block= Node('block','block',lines)
            case = Node(compare,'case',[block])
            children.append(case) 

        if next=='default:':
            self.index+=len('default:')
            lines=[]
            while True:
                line= self.getExpression(_break=';')
                if line is not None :lines.append(line)
                if self.current == '}': break
            block= Node('block','block',lines)
            default = Node('default','default',[block])
            children.append(default) 
        
        if self.current == '}': self.index+=1

        options= Node('options','options',children)
        return Node('switch','switch',[value,options])     

    def getWhileBlock(self):
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';')
        return Node('while','while',[condition,block])

    def getForBlock(self):
        first= self.getExpression(_break=';')
        if self.previous==';':
            condition= self.getExpression(_break=';')
            increment= self.getExpression(_break=')')
            if  self.current == '{':
                self.index+=1  
                block= self.getBlock()
            else:
                block= self.getExpression(_break=';')
            return Node('for','for',[first,condition,increment,block])   
        elif self.nextIs('in'):
            self.index+=2
            # si hay espacios luego del in debe eliminarlos
            while self.current == ' ':self.index+=1
            list= self.getExpression(_break=')')
            if  self.current == '{':
                self.index+=1  
                block= self.getBlock()
            else:
                block= self.getExpression(_break=';')
            return Node('forIn','forIn',[first,list,block])       

    def getFunction(self):
        name=  self.getValue()
        if self.current == '(': self.index+=1
        listArgs=  self.getArgs(end=')')
        block = self.getControlBlock()
        args =Node('args','args',listArgs) 
        return Node(name,'function',[args,block]) 

    def getChildFunction(self,name,parent):        
        if name in self.arrowFunction:
            variableName= self.getValue()
            if variableName=='' and self.current==')':
                self.index+=1
                return Node(name,'arrowFunction',[parent]) 
            else:    
                if self.current=='=' and self.next == '>':self.index+=2
                else:raise Exception('map without body')
                variable= Node(variableName,'variable')
                body= self.getExpression(_break=')')
                return Node(name,'arrowFunction',[parent,variable,body])        
        else: 
            args=  self.getArgs(end=')')
            args.insert(0,parent)
            return  Node(name,'childFunction',args)

    def getReturn(self): 
        value= self.getExpression(_break=';')
        return Node('return','return',[value])  

    def getTryCatchBlock(self):
        children = []              
        tryBlock = self.getControlBlock()
        children.append(tryBlock)
        if self.nextIs('catch'):
            self.index+=len('catch')
            if self.current == '(':
                self.index+=1
                variable= self.getExpression(_break=')')
            catchBlock = self.getControlBlock()
            catch = Node('catch','catch',[variable,catchBlock])
            children.append(catch)
        if self.current == ';':self.index+=1
        return Node('try','try',children)    

    def getThrow(self): 
        exception= self.getExpression(_break=';')
        return Node('throw','throw',[exception])            

    def getIndexOperand(self,name):
        idx= self.getExpression(_break=']')
        operand= Node(name,'variable')
        return Node('[]','operator',[operand,idx]) 

    def getEnum(self,value):
        if '.' in value and self.model.isEnum(value):
            names = value.split('.')
            enumName = names[0]
            enumOption = names[1] 
            enumValue= self.model.getEnumValue(enumName,enumOption)
            return Node(enumValue,'constant')
        else:
            values= self.model.getEnum(value)
            attributes= []
            for name in values:
                _value = values[name]
                # _valueType = type(_value).__name__
                attribute = Node(name,'keyValue',[Node(_value,'constant')])
                attributes.append(attribute)
            return Node('object','object',attributes)

 