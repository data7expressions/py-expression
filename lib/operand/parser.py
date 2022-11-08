from lib2to3.pgen2.token import OP
from typing import List, Tuple
import numpy as np
from lib.contract.base import *
from lib.contract.operands import Operand, OperandType
from lib.contract.type import Type
from lib.contract.managers import IModelManager
from lib.helper.h3lp import h3lp

class Parser():
    def __init__(self,model:IModelManager,expression:str):
       self.model = model
       self.positions = self.normalize(expression)       
       self.buffer = list(map(lambda p: p[0], self.positions))
       self.length=len(self.buffer)
       self.index=0
       self.singleOperators = []
       self.doubleOperators = []
       self.tripleOperators = [] 
       self.assignmentOperators = []
       for p in self.model.operators:
            key = p[0]
            if len(key)==1: 
                self.singleOperators.append(key)
            elif len(key)==2: 
                self.doubleOperators.append(key)
                if p[1].priority == 1:
                    self.assignmentOperators.append(key) 
            elif len(key)==3: 
                self.tripleOperators.append(key)        
    
    def parse(self)->Operand:
        operands=[]
        while not self.end:
            operand =self.getExpression(_break=';')
            if operand is None:break
            operands.append(operand)
        if len(operands)==1 :
            return operands[0]
        return Operand(Position(0,0),'block', OperandType.Block,operands)

    def getExpression(self,operand1=None,operator=None,_break='')->Operand:
        expression = None
        operand2 = None
        isBreak = False
        pos = self.pos()               
        while not self.end:
            if operand1 is None and operator is None: 
                operand1=  self.getOperand()
                operator= self.getOperator()
                if operator is None or self.current in _break:
                    if self.current != None and self.current in _break:
                        self.index+=1
                    expression = operand1
                    isBreak= True
                    break
            operand2=  self.getOperand()
            nextOperator= self.getOperator()
            if operator is not None and operand1 is not None:
                if nextOperator is None or self.current in _break:
                    if self.current != None and self.current in _break:
                        self.index+=1
                    expression= Operand(self.pos(len(operator)), operator,OperandType.Operator,[operand1,operand2])
                    isBreak= True
                    break
                elif self.model.priority(operator)>=self.model.priority(nextOperator):
                    operand1=Operand(self.pos(len(operator)), operator,OperandType.Operator,[operand1,operand2])
                    operator=nextOperator
                else:
                    operand2 = self.getExpression(operand1=operand2,operator=nextOperator,_break=_break)
                    expression= Operand(self.pos(len(operator)), operator,OperandType.Operator,[operand1,operand2])
                    isBreak= True
                    break
        if not isBreak and operand1 is not None and operand2 is not None:
            expression=Operand(pos, operator,OperandType.Operator,[operand1,operand2])
        return expression  

    def getOperand(self)-> Operand:        
        isNegative=False
        isNot=False
        isBitNot=False
        operand=None
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
        pos = self.pos()
        if char.isalnum():    
            value=  self.getValue()
            if value=='function' and self.current == '(': 
                self.index+=1
                operand = self.getFunctionBlock(pos)
            elif value=='if' and self.current == '(': 
                self.index+=1
                operand = self.getIfBlock(pos)
            elif value=='for' and self.current == '(': 
                self.index+=1
                operand = self.getForBlock(pos)    
            elif value=='while' and self.current == '(': 
                self.index+=1
                operand = self.getWhileBlock(pos)   
            elif value=='switch' and self.current == '(': 
                self.index+=1
                operand = self.getSwitchBlock(pos)
            elif not self.end and self.current == '(':
                self.index+=1
                if '.' in value:
                    names = value.split('.')
                    name = names.pop()
                    variableName= '.'.join(names)
                    variable = Operand(pos,variableName,OperandType.Var)
                    operand= self.getChildFunc(name,variable)
                else:
                    args=  self.getArgs(end=')')
                    operand= Operand(pos,value,OperandType.CallFunc,args) 
            elif value=='try' and self.current == '{':
                operand = self.getTryCatchBlock(pos)  
            elif value=='throw':   
                operand = self.getThrow(pos)
            elif value=='return':   
                operand = self.getReturn(pos)    
            elif value=='break':                
                operand = Operand(pos,'break',OperandType.Break)
            elif value=='continue':                
                operand = Operand(pos,'continue',OperandType.Continue)
            elif not self.end and self.current == '[':                
                self.index+=1
                operand = self.getIndexOperand(value) 
            elif h3lp.validator.isIntegerFormat(value): 
                if isNegative:
                    value = int(value)* -1
                    isNegative= False 
                elif isBitNot:
                    value = ~ int(value)
                    isBitNot= False     
                else:
                    value =int(value)
                operand = Operand(pos,value,OperandType.Const,[], Type.integer())
            elif h3lp.validator.isDecimalFormat(value):
                if isNegative:
                    value = float(value)* -1
                    isNegative= False
                elif isBitNot:
                    value = ~float(value)
                    isBitNot= False      
                else:
                    value =float(value)
                operand = Operand(pos,value,OperandType.Const,[], Type.decimal())
            elif self.model.isConstant(value):
                constantValue = self.model.getConstantValue(value)                
                operand = Operand(pos,constantValue,OperandType.Const,[], Type.get(constantValue))                
            elif self.model.isEnum(value):                
                operand= self.getEnum(value)
            else:
                operand = Operand(pos,value,OperandType.Var)
        elif char == '\'' or char == '"':
            self.index+=1
            result=  self.getString(char)
            operand= Operand(pos,result,OperandType.Const, [], Type.string() )
        elif char == '`':
            self.index+=1
            result=  self.getTemplate()
            operand= Operand(pos,result,OperandType.Template, [], Type.string() )    
        elif char == '(':
            self.index+=1
            operand=  self.getExpression(_break=')') 
        elif char == '{':
            self.index+=1
            operand = self.getObject(pos)  
        elif char == '[':
            self.index+=1
            elements=  self.getArgs(end=']')
            operand =  Operand(pos,'array',OperandType.List,elements)        
        elif char == '$':
            if self.offset(1) == '{':
                self.index+=2
                variableName = self.getValue()
                if not self.end and self.nextIs('}'):
                    self.index+=1
                else:
                    raise Exception('Not found character "}" in Environment variable '+variableName)
            else:
                self.index+=1
                variableName = self.getValue()
            operand = Operand(pos,variableName,OperandType.Env)
        
        if operand is None:
            raise Exception('Operand undefined')        
        operand = self.solveChain(operand, pos)
        if isNegative:operand= Operand(Position(pos.ln,pos.col-1),'-',OperandType.Operator,[operand])
        if isNot:operand=Operand(Position(pos.ln,pos.col-1),'!',OperandType.Operator,[operand])
        if isBitNot:operand=Operand(Position(pos.ln,pos.col-1),'~',OperandType.Operator,[operand])  
        return operand

    def solveChain(self,operand, pos:Position)->Operand:
        if self.end:
            return operand        
        if self.current == '.':
            self.index+=1
            name=  self.getValue()            
            if self.current == '(': 
                self.index+=1
                if '.' in name:
                    # .xxx.xxx(p=> p.xxx)
                    names = np.array(h3lp.obj.names(name))
                    propertyName = ''.join(names[0:len(names)-2])
                    functionName = names[len(names)-2,len(names)-1]
                    property = Operand(pos, propertyName, OperandType.Property, [operand])
                    return self.solveChain(self.getChildFunc(functionName, property), pos)
                else:
                    # .xxx(p=> p.xxx)
                    return self.solveChain(self.getChildFunc(name, operand), pos) 
            elif self.current == '[':
                self.index+=1 
                if '.' in name:
                    # .xxx.xxx[x]
                    property = Operand(pos, name, OperandType.Property, [operand])
                    idx = self.getExpression(_break= ']')
                    return Operand(pos, '[]', OperandType.Operator, [property, idx])
                else:
                    # .xxx[x]
                    property = Operand(pos, name, OperandType.Property, [operand])
                    idx = self.getExpression(_break= ']')
                    return Operand(pos, '[]', OperandType.Operator, [property, idx])      
            else:
                # .xxx
                return Operand(pos, name, OperandType.Property, [operand])
        elif self.current == '[':
            # xxx[x][x] or xxx[x].xxx[x]
            self.index += 1
            idx = self.getExpression(_break= ']')
            return Operand(pos, '[]', OperandType.Operator, [operand, idx])
        else:
            return operand      

    def getOperator(self):
        if self.end:
            return None
        op=None
        if self.index+2 < self.length:
            triple = self.current+self.offset(1)+self.buffer[self.index+2]
            if triple in self.tripleOperators :
                op=triple
        if op is None and  self.index+1 < self.length:
            double = self.current+self.offset(1)
            if double in self.doubleOperators:
                op=double
        if op is None:
            if not self.model.isOperator(self.current):
                return None 
            op=self.current
        self.index+=len(op)
        return op
    
    def normalize(self,expression:str)->List[str]:
        isString=False
        quotes=None
        buffer = list(expression)
        length=len(buffer)
        result:List[Tuple[str, int, int]] =[]
        line = 0
        col = 0
        i=0
        while i < length:
            p =buffer[i]        
            if isString and p == quotes: 
                isString=False 
            elif not isString and (p == '\'' or p=='"' or p=='`' ):
                isString=True
                quotes=p
            if isString:
                result.append((p, line, col))
            elif  p == ' ' :
                # solo debería dejar los espacios cuando es entre caracteres alfanuméricos. 
                # por ejemplo en el caso de "} if" no debería quedar un espacio 
                if i+1 < length and h3lp.validator.isAlphanumeric(buffer[i-1]) and h3lp.validator.isAlphanumeric(buffer[i+1]):
                    result.append((p, line, col))                
            elif (p == '\n'):
               line+= 1
               col = 0
            elif (p!='\r' and p!='\t' ):
               result.append((p, line, col)) 
            i+=1
            col+=1
        if result[len(result)-1] == ';':
            return result[0:len(result)-2]   
        return result
    
    @property
    def end(self)->bool:
        return self.index >= self.length     
    
    @property
    def current(self)->str:
        return self.buffer[self.index] if self.index < self.length else None    
    
    def offset(self, offset=0)->str:
        return self.buffer[self.index + offset] if self.index + offset < self.length else None

    def pos (self, offset=0)-> Position:
        if self.index + offset < self.length and self.index + offset > -1:
            position = self.positions[self.index - offset]
            return Position(position[1], position[2])
        else:
            return None

    def nextIs(self,key)->bool:
        arr = list(key)        
        for i, p in enumerate(arr):
            if self.buffer[self.index+i] != p:
                return False
        return True     

    def getValue(self,increment:bool=True)->str:
        buff=[]
        if increment:
            while not self.end and h3lp.validator.isAlphanumeric(self.current):
                buff.append(self.current)
                self.index+=1            
        else:
            index = self.index
            while not self.end and h3lp.validator.isAlphanumeric(self.buffer[index]):
                buff.append(self.buffer[index])
                index+=1        
        return ''.join(buff)

    def getString(self,char)->str:
        buff=[]       
        while not self.end :
            if self.current == char:
                if not((self.index+1 < self.length and self.next == char) or (self.previous == char)):
                    break 
            buff.append(self.current)
            self.index+=1
        self.index+=1    
        return ''.join(buff)

    def getTemplate(self)->str:
        buff=[]       
        while not self.end :
            if self.current == '`':                
                break 
            buff.append(self.current)
            self.index+=1
        self.index+=1    
        return ''.join(buff)

    def getArgs(self,end=')')->List[Operand]:
        args= []
        while True:
            arg= self.getExpression(_break=','+end)
            if arg is not None:args.append(arg)
            if self.offset(-1)==end: break
        return args

    def getObject(self,pos:Position)->Operand:
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
            keyValPos= self.pos()
            value= self.getExpression(_break=',}')
            attribute = Operand(keyValPos,name,OperandType.keyValue,[value])
            attributes.append(attribute)
            if self.previous=='}':
                break
        
        return  Operand(pos,'obj',OperandType.Obj,attributes) 

    def getBlock(self)->Operand:
        blockPos = self.pos()
        lines= []
        while True:
            line= self.getExpression(_break=';}')
            if line is not None :
                lines.append(line)
            if self.offset(-1) ==';' and self.current == '}':
                self.index += 1
                break
            if self.offset(-1) == '}':
                break       
        return Operand(blockPos,'block',OperandType.Block,lines) 

    def getControlBlock(self)->Operand:
        if  self.current == '{':
            self.index+=1  
            return self.getBlock()
        else:
            return self.getExpression(_break=';')

    def getReturn(self,pos:Position)-> Operand: 
        value= self.getExpression(_break=';')
        return Operand(pos,'return',OperandType.Return,[value])  

    def getTryCatchBlock(self,pos:Position)->Operand:
        children = []              
        tryBlock = self.getControlBlock()
        children.append(tryBlock)
        if self.nextIs('catch'):
            catchChildren=[]
            catchPos = self.pos(len('catch'))
            self.index+=len('catch')
            if self.current == '(':
                self.index+=1
                variable= self.getExpression(_break=')')
                catchChildren.append(variable)
                
            catchBlock = self.getControlBlock()
            catchChildren.append(catchBlock)
            catch = Operand(catchPos,'catch',OperandType.Catch,[variable,catchBlock])
            children.append(catch)
        if self.current == ';':self.index+=1
        return Operand(pos,'try',OperandType.Try,children)    

    def getThrow(self,pos:Position)->Operand: 
        exception= self.getExpression(_break=';')
        return Operand(pos,'throw',OperandType.Throw,[exception])            

    def getIfBlock(self,pos:Position)->Operand:
        children = []
        condition= self.getExpression(_break=')')
        children.append(condition)
        block = self.getControlBlock()
        children.append(block)
        while self.nextIs('else if('):
            elseIfPos = self.pos()
            self.index+=len('else if(')
            condition= self.getExpression(_break=')')
            block = self.getControlBlock()
            elifNode = Operand(elseIfPos,'elseif',OperandType.ElseIf,[condition,block])
            children.append(elifNode)
        if self.nextIs('else'):
            self.index+=len('else')
            elseBlock = self.getControlBlock()           
            children.append(elseBlock)
        return Operand(pos,'if',OperandType.If,children)   
        
    def getSwitchBlock(self,pos:Position)->Operand:
        children = []
        value= self.getExpression(_break=')')
        children.append(value)        
        if self.current == '{': self.index+=1
        if self.nextIs('case'):next='case'
        elif self.nextIs('default:'):next='default:'
        else: next=''        
        while next=='case':
            self.index+=len('case')
            if self.current == '\'' or self.current == '"':
                char = self.current
                self.index+=1
                compare=  self.getString(char)
            else:    
                compare= self.getValue()

            caseNode = Operand(self.pos(), compare, OperandType.Case)
            block = Operand(self.pos(), 'block', OperandType.Block)
            caseNode.children = [block]    
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
            block.children = lines
            children.append(caseNode) 

        if next=='default:':
            self.index+=len('default:')
            defaultNode = Operand(self.pos(), 'default', OperandType.Default)
            block = Operand(self.pos(), 'block', OperandType.Block)
            defaultNode.children = [block]
            lines=[]
            while True:
                line= self.getExpression(_break=';')
                if line is not None :lines.append(line)
                if self.current == '}': break
            block.children = lines
            children.append(defaultNode) 
        
        if self.current == '}': self.index+=1   
        return Operand(pos,'switch',OperandType.Switch,children)     

    def getWhileBlock(self,pos:Position)->Operand:
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';')
        return Operand(pos,'while',OperandType.While,[condition,block])

    def getForBlock(self,pos:Position)->Operand:
        first= self.getExpression(_break=';')
        if self.previous==';':
            condition= self.getExpression(_break=';')
            increment= self.getExpression(_break=')')
            if  self.current == '{':
                self.index+=1  
                block= self.getBlock()
            else:
                block= self.getExpression(_break=';')
            return Operand(pos,'for', OperandType.For,[first,condition,increment,block])   
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
            return Operand(pos,'forIn',OperandType.ForIn,[first,list,block])       
        raise Exception('expression for error') 
        
    def getFunctionBlock(self, pos:Position)->Operand:
        name=  self.getValue()
        if self.current == '(': self.index+=1
        argsPos = self.pos()
        args=  self.getArgs(end=')')
        block = self.getControlBlock()
        argsOperand =Operand(argsPos,'args',OperandType.Args,args) 
        return Operand(pos,name,'function',[argsOperand,block]) 

    def getChildFunc(self,name,parent)->Operand:
        isArrow = False
        pos = self.pos()
        variableName = self.getValue(False)
        if variableName != '':
			# example: p => {name:p.name}
			# example: p -> {name:p.name}
            i = len(variableName)
            if (self.offset(i) == '=' or self.offset(i) == '-') and  self.offset(i + 1) == '>':
                isArrow = True
                self.index += (len(variableName) + 2) # [VARIABLE+NAME] + [=>]			
        elif self.current + self.offset(1) == '()':
		    #  example: ()=> {name:name}
			#  example: ()-> {name:name}
            if (self.offset(2) == '=' or self.offset(2) == '-') and self.offset(3) == '>':
                isArrow = True
                self.index += 4 # [()=>]			
        elif self.current + self.offset(1) == '=>' or self.current + self.offset(1) == '->':
			#  example: => {name:name}
			#  example: -> {name:name}
            isArrow = True
            self.index += 2 # [=>]		
          
        if isArrow:
            variable = Operand(pos, variableName, OperandType.Var)
            body = self.getExpression(None, None, ')')
            return Operand(pos, name, OperandType.Arrow, [parent, variable, body])      
        else:
            if self.current == ')':
                self.index += 1
                # Example: xxx.xxx()
                return Operand(pos, name, OperandType.ChildFunc, [parent])
            # Example: xxx.xxx(x)
            args=  self.getArgs(end=')')
            args.insert(0,parent)
            return  Operand(pos,name,OperandType.ChildFunc,args)
   
    def getIndexOperand(self,name, pos:Position)->Operand:
        idx= self.getExpression(_break=']')
        operand= Operand(pos,name,OperandType.Var)
        return Operand(pos,'[]', OperandType.Operator,[operand,idx]) 

    def getEnum(self,value, pos:Position)->Operand:
        if '.' in value and self.model.isEnum(value):
            names = value.split('.')
            enumName = names[0]
            enumOption = names[1] 
            enumValue= self.model.getEnumValue(enumName,enumOption)
            return Operand(pos,enumValue,OperandType.Const, [], Type.get(value))
        else:
            values= self.model.getEnum(value)
            attributes= []
            for name in values:
                _value = values[name]
                # _valueType = type(_value).__name__
                attribute = Operand(pos,name,OperandType.KeyVal,[Operand(pos,_value,OperandType.Const,[],Type.get(_value))])
                attributes.append(attribute)
            return Operand(pos,'obj',OperandType.Obj,attributes)
 