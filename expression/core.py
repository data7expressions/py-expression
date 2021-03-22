import re
# from typing import ChainMap

class Operand():
    @property
    def value(self): 
        pass

class Constant(Operand):
    def __init__(self,value ):
      self._value  = value
    @property
    def value(self): 
        return self._value 
class Variable(Operand):
    def __init__(self,name ):
      self._name  = name
      self._context  = None

    @property
    def context(self):
        return self._context
    @context.setter
    def context(self,value):
        self._context=value

    @property
    def value(self):
        return self._context[self._name]
    @value.setter
    def value(self,value):
        self._context[self._name]=value       
class Function(Operand):
    def __init__(self,function,args):
      self.args  = args
      self.function  = function

    @property
    def value(self): 
        args=[]
        for p in self.args:args.append(p.value)
        return self.function(*args)
class Operator(Operand):
    def __init__(self,operands ):
      self._operands  = operands

    @property
    def operands(self):
        return self._operands

    @property
    def value(self):
        val=self._operands[0].value
        l=len(self._operands)
        i=1
        while i<l:
            val=self.solve(val,self._operands[i].value)
            i+=1
        return val  

    def solve(self,a,b):
        pass 

class ExpManager():
    def __init__(self):
       self.operators={} 
       self.functions={}
       self.RE_INT = re.compile('^[0-9]+$')
       self.RE_FLOAT = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')

    def add(self,k,imp):
        self.operators[k]=imp
    def addFunction(self,k,imp):
        self.functions[k]=imp    

    def new(self,k,operands):
        return self.operators[k](operands)

    def setContext(self,expression,context):
        if hasattr(expression, 'operands'):
            for p in expression.operands:
                if isinstance(p,Variable):
                    p.context = context
                elif hasattr(p, 'operands'):
                    self.setContext(p,context)    

    def solve(self,string:str,context:dict=None):        
        expression=self.parse(string)
        if context != None:
            self.setContext(expression,context)
        return expression.value


    def parse(self,string):
        chars = list(string)
        operand,index= self.getOperand(chars)
        return operand

    def getOperand(self,chars,index=0,parenthesis=False):
        buff = []
        lastOperator= None
        alter=None
        operators=[]
        operands=[]
        operand=None
        strOperators = set('+-*/%=<>$|!^~()')
        strOperatorsFirst = set('*/')
        strOperatorsSecond = set('+-')  

        length=len(chars)
        while index < length :
            char=chars[index]
            index+=1         
            if char not in strOperators:
                buff.append(char)
            else:    
                value=''.join(buff)
                if char == '(' and value=='':
                    operand,index = self.getOperand(chars,index,parenthesis=True)
                    operands.append(operand)
                elif value=='': 
                    if char == '-':
                       alter = lambda x : x * -1 # exp: 2*-1
                    else:    
                        lastOperator+=char  # exp: **,//,==,!= etc
                else:
                    operand=self.getTerminalOperand(value,alter)
                    if char == ')':
                        if lastOperator == None:
                            return operand, index
                        else:    
                            operands.append(operand)
                            return self.new(lastOperator,operands),index                       
                    elif lastOperator != None and lastOperator!=char: # in case a+b+c utiliza un solo operador con multiples operandos
                        if char in strOperatorsFirst and lastOperator in strOperatorsSecond:
                            nextOperand,index = self.getOperand(chars,index)  
                            operands.append(self.new(char,[operand,nextOperand]))
                            return self.new(lastOperator,operands),index
                        else:
                            operands.append(operand)    
                            operands=[self.new(lastOperator,operands)]
                    else:
                        operands.append(operand)
                    lastOperator=char
                    buff=[]

        value=''.join(buff)
        operand=self.getTerminalOperand(value,alter)
        if lastOperator == None:
            return operand, index
        else:    
            operands.append(operand) 
            return self.new(lastOperator,operands) , index

    def getTerminalOperand(self,value,alter):
        if(self.RE_FLOAT.match(value)): # exp: 1, 23, 2.6
            return self.getConstant(value,alter)
        else:    
            return self.new('variable',value) # exp: a, x, y, name
   
    def getConstant(self,value,alter):
        result=None
        if self.RE_INT.match(value): 
            result= alter(int(value)) if alter!= None else int(value)
        elif self.RE_FLOAT.match(value):
            result=  alter(float(value)) if alter!= None else float(value)
        else:
            result=  alter(value) if alter!= None else value
        return self.new('constant',result)  


class Addition(Operator):
    def solve(self,a,b):
        return a+b 
class Subtraction (Operator):
    def solve(self,a,b):
        return a-b   
class Multiplication(Operator):
    def solve(self,a,b):
        return a*b 
class Division (Operator):
    def solve(self,a,b):
        return a/b  
class Exponentiation(Operator):
    def solve(self,a,b):
        return a**b 
class FloorDivision (Operator):
    def solve(self,a,b):
        return a//b   
class Mod (Operator):
    def solve(self,a,b):
        return a%b 

class Equal(Operator):
    def solve(self,a,b):
        return a==b
class NotEqual(Operator):
    def solve(self,a,b):
        return a!=b          
class GreaterThan(Operator):
    def solve(self,a,b):
        return a>b
class LessThan(Operator):
    def solve(self,a,b):
        return a<b 
class GreaterThanOrEqual(Operator):
    def solve(self,a,b):
        return a>=b
class LessThanOrEqual(Operator):
    def solve(self,a,b):
        return a<=b                

class And(Operator):
    def solve(self,a,b):
        return a and b   
class Or(Operator):
    def solve(self,a,b):
        return a or b 
class Not(Operator):
    @property
    def value(self):
        return not self._operands[0].value

class BitAnd(Operator):
    def solve(self,a,b):
        return a & b 
class BitOr(Operator):
    def solve(self,a,b):
        return a | b
class BitXor(Operator):
    def solve(self,a,b):
        return a ^ b                  
class BitNot(Operator):
    @property
    def value(self):
        return ~ self._operands[0].value
class LeftShift(Operator):
    def solve(self,a,b):
        return a << b   
class RightShift(Operator):
    def solve(self,a,b):
        return a >> b   

exp = ExpManager()
exp.add('constant',Constant)
exp.add('variable',Variable)
exp.add('function',Function)

exp.add('+',Addition)
exp.add('-',Subtraction)
exp.add('*',Multiplication)
exp.add('/',Division)
exp.add('**',Exponentiation)
exp.add('//',FloorDivision)
exp.add('%',Mod)

exp.add('==',Equal)
exp.add('!=',NotEqual)
exp.add('>',GreaterThan)
exp.add('<',LessThan)
exp.add('>=',GreaterThanOrEqual)
exp.add('<=',LessThanOrEqual)

exp.add('&&',And)
exp.add('||',Or)
exp.add('!',Not)

exp.add('&',BitAnd)
exp.add('|',BitOr)
exp.add('^!',BitXor)
exp.add('~',BitNot)
exp.add('<<',LeftShift)
exp.add('>>',RightShift)

def nvl(a,b): return a if a else b

exp.addFunction('nvl',nvl)

# result=exp.solve('(1+4)*2')
# print(result)


