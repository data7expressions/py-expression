import re
from .base import *
from .coreLib import CoreLib


class ModelManager():
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
            self.addEnum(name,library.enums[name])

        for name in library.operators:
            operator= library.operators[name]
            for cardinality in operator:
                data = operator[cardinality]
                self.addOperator(name,cardinality,data['metadata'])    

        for name in library.functions:
            data = library.functions[name]
            self.addFunction(name,data['metadata'])

    def addEnum(self,key,source):
        self._model.enums[key]=source
    def isEnum(self,name):    
        names = name.split('.')
        return names[0] in self._model.enums.keys()
    def getEnumValue(self,name,option): 
        return self._model.enums[name][option]
    def getEnum(self,name): 
        return self._model.enums[name]
  
    def addOperator(self,name:str,cardinality:int,metadata):
        if name not in self._model.operators.keys():
            self._model.operators[name]= {}    
        self._model.operators[name][cardinality] = metadata       

    def getOperator(self,name:str,cardinality:int):
        try:
            metadata = self.getOperatorMetadata(name,cardinality)
            if metadata['lib'] in self._libraries:
                return self._libraries[metadata['lib']].operators[name][cardinality]['source']
            return None        
        except:
            raise ModelError('error with operator: '+name)  

    def getOperatorMetadata(self,name:str,cardinality:int):
        try:            
            if name in self._model.operators:
                operator = self._model.operators[name]
                if cardinality in operator:
                    return operator[cardinality]
            return None        
        except:
            raise ModelError('error with operator: '+name)             

    def priority(self,name:str,cardinality:int)->int:
        try:
            metadata = self.getOperatorMetadata(name,cardinality)
            return metadata["priority"] if metadata is not None else -1
        except:
            raise ModelError('error to priority : '+name)        

    def addFunction(self:str,name:str,metadata):
        self._model.functions[name] = metadata

    def getFunction(self,name:str):
        try:            
            metadata = self.getFunctionMetadata(name)
            if metadata['lib'] in self._libraries:
                return self._libraries[metadata['lib']].functions[name]['source']
            return None
        except:
            raise ModelError('error with function: '+name)      

    def getFunctionMetadata(self,name:str):
        try:
            if name in self._model.functions:
                return self._model.functions[name]
            return None
        except:
            raise ModelError('error with function: '+name)        


# Facade   
class Exp(metaclass=Singleton):
    def __init__(self):
       self.reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$') 
       self.reInt = re.compile('[0-9]+$')
       self.reFloat = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')
       self._tripleOperators = []
       self._doubleOperators = [] 
       self._assigmentOperators = [] 
       self._modelManager = ModelManager(Model())
       self.addLibrary(CoreLib())        


    def addLibrary(self,library):
        self._modelManager.addLibrary(library)
        self.refresh() 
    
    def refresh(self):
        for key in self._modelManager.model.operators.keys():
            if len(key)==2: self._doubleOperators.append(key)
            elif len(key)==3: self._tripleOperators.append(key)

            operator = self._modelManager.model.operators[key]
            if 2 in operator.keys():
               if operator[2]['category'] == 'assignment':
                  self._assigmentOperators.append(key)

    @property
    def doubleOperators(self):
        return self._doubleOperators

    @property
    def tripleOperators(self):
        return self._tripleOperators   

    def newOperator(self,name:str,operands:list[Operand])->Operator:
        try: 
            args = len(operands)
            if args == 1:
                return UnitaryOperator(name,operands,self)
            elif args == 2:
                if name == '&&':
                    return And(name,operands,self)
                elif name == '||':
                    return Or(name,operands,self)
                elif name in self._assigmentOperators:
                    return AssigmentOperator(name,operands,self)      
                else:
                    return BinaryOperator(name,operands,self) 
            elif args == 3:
                return TernaryOperator(name,operands,self) 
            else:
                return Operator(name,operands,self) 
        except:
            raise ExpressionError('error with operator: '+name) 

    def getOperator(self,name:str,cardinality:int):
        return self._modelManager.getOperator(name,cardinality)
    def priority(self,name:str,cardinality:int)->int:
        return self._modelManager.priority(name,cardinality)
  
    def isEnum(self,name):    
        return self._modelManager.isEnum(name) 
    def getEnumValue(self,name,option): 
        return self._modelManager.getEnumValue(name,option) 
    def getEnum(self,name): 
        return self._modelManager.getEnum(name) 
    
    def getFunction(self,name):
        return self._modelManager.getFunction(name)

      
    
    def minify(self,expression:str)->str:
        isString=False
        quotes=None
        result =[]
        buffer = list(expression)
        for p in buffer:
            if isString and p == quotes: isString=False 
            elif not isString and (p == '\'' or p=='"'):
                isString=True
                quotes=p
            if (p != ' ' and p!='\n' and p!='\r' and p!='\t' ) or isString:
               result.append(p)
        return result
    
    def parse(self,expression)->Operand:
        try:            
            parser = Parser(self,self.minify(expression))
            operand= parser.parse() 
            del parser
            return operand  
        except Exception as error:
            raise ExpressionError('expression: '+expression+' error: '+str(error))

    def eval(self,operand:Operand,context:dict={})-> any :  
        if context is not None:
            self.setContext(operand,Context(context))
        return operand.value

    def debug(self,operand:Operand,token:Token,context:dict={}):
        if context is not None:
            self.setContext(operand,Context(context))
        operand.debug(token,0)

    def solve(self,expression:str,context:dict={})-> any :
        operand=self.parse(expression)
        return self.eval(operand,context)

    def serialize(self,operand:Operand)-> dict:        
        if len(operand.operands)==0:return {'n':operand.name,'t':type(operand).__name__}
        children = []                
        for p in operand.operands:
            children.append(self.serialize(p))
        return {'n':operand.name,'t':type(operand).__name__,'c':children}     

    def deserialize(self,serialized:dict)-> Operand:
        children = []
        if 'c' in serialized:
            for p in serialized['c']:
                children.append(self.deserialize(p))
        return  eval(serialized['t'])(serialized['n'],children,self) 

 
    def getOperandByPath(self,operand:Operand,path)->Operand:
        search = operand
        for p in path:
            if len(search.operands) <= p:return None
            search = search.operands[p]
        return search    

        
    def setContext(self,operand:Operand,context:Context):
        if issubclass(operand.__class__,Contextable):operand.context = context         
        if len(operand.operands)>0 :       
            for p in operand.operands:
                if issubclass(p.__class__,Contextable):p.context = context                
                if len(p.operands)>0:
                    self.setContext(p,context)

    def setParent(self,operand:Operand,parent:Operand=None,index:int=0):
        operand.parent = parent
        operand.index = index
        if  len(operand.operands)>0:
            for i,p in enumerate(operand.operands):
                self.setParent(p,operand,i) 

    def getVars(self,operand:Operand)->dict:
        self.setParent(operand)
        return self._getVars(operand)        

    def _getVars(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Variable):
            list[operand.name] = self.getVarType(operand)
        for p in operand.operands:
            if isinstance(p,Variable):
                list[p.name] = self.getVarType(p)
            elif len(p.operands)>0:
                subList= self._getVars(p)
                list = {**list, **subList}
        return list 

    def getVarType(self,operand:Operand)->str:
        return self.getOperandType(operand.parent,operand.index)

    def getOperandType(self,parent:Operand,index)->str:
        """ """
        if isinstance(parent,Operator):
            metadata = self._modelManager.getOperatorMetadata(parent.name,len(parent.operands))
            if metadata['category'] == 'comparison':
                otherIndex = 1 if index == 0 else 0
                otherOperand= parent.operands[otherIndex]
                if isinstance(otherOperand,Constant):
                    return otherOperand.type
                elif isinstance(otherOperand,Function):    
                    pass
                # TODO continuar
            else:        
                return metadata['args'][index]['type']
        elif isinstance(parent,Function):
            name = parent.name.replace('.','',1) if parent.name.starWith('.') else  parent.name
            metadata =self._modelManager.model.functions[name]
            return metadata['args'][index]['type'] 

    def getConstants(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Constant):
            list[operand.value] = operand.type
        for p in operand.operands:
            if isinstance(p,Constant):
                list[p.value] = p.type
            elif len(p.operands)>0:
                subList= self.getConstants(p)
                list = {**list, **subList}
        return list
    
    def getOperators(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Operator):
            metadata = self._modelManager.getOperatorMetadata(operand.name,len(operand.operands)) 
            list[operand.name] = metadata['category']
        for p in operand.operands:
            if isinstance(p,Operator):
                metadata = self._modelManager.getOperatorMetadata(p.name,len(p.operands)); 
                list[p.name] =  metadata['category']
            elif len(p.operands)>0:
                subList= self.getOperators(p)
                list = {**list, **subList}
        return list

    def getFunctions(self,operand:Operand)->dict:
        list = {}
        if isinstance(operand,Function):
            list[operand.name] = {}
        for p in operand.operands:
            if isinstance(p,Function):
                list[p.name] = {}
            elif len(p.operands)>0:
                subList= self.getFunctions(p)
                list = {**list, **subList}

        for key in list:
            list[key] = self._modelManager.model.functions[key]
        return list

    def getMetadata(self,operand:Operand)->dict:
        
        if isinstance(operand,Operator):
            pass
        elif isinstance(operand,Function):
            pass
        elif isinstance(operand,Constant):
            pass    
        elif isinstance(operand,Variable):
            pass
    
 
class Parser():
    def __init__(self,mgr,expression):
       self.mgr = mgr 
       self.buffer = list(expression)
       self.length=len(self.buffer)
       self.index=0
    
    def parse(self):
        operands=[]
        while not self.end:
            operand =self.getExpression(_break=';')
            if operand is None:break
            operands.append(operand)
        if len(operands)==1 :
            return operands[0]
        return Block('block',operands,self.mgr) 

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

    def getExpression(self,operand1=None,operator=None,_break=''):
        expression = None
        operand2 = None
        isbreak = False               
        while not self.end:
            if operand1 is None and operator is None: 
                operand1=  self.getOperand()
                operator= self.getOperator()
                if operator is None or operator in _break: 
                    expression = operand1
                    isbreak= True
                    break
            operand2=  self.getOperand()
            nextOperator= self.getOperator()
            if nextOperator is None or nextOperator in _break:
                expression= self.mgr.newOperator(operator,[operand1,operand2])
                isbreak= True
                break
            elif self.priority(operator)>=self.priority(nextOperator):
                operand1=self.mgr.newOperator(operator,[operand1,operand2])
                operator=nextOperator
            else:
                operand2 = self.getExpression(operand1=operand2,operator=nextOperator,_break=_break)
                expression= self.mgr.newOperator(operator,[operand1,operand2])
                isbreak= True
                break
        if not isbreak: expression=self.mgr.newOperator(operator,[operand1,operand2])
        # if all the operands are constant, reduce the expression a constant 
        if expression is not None and len(expression.operands)>0:    
            allConstants=True              
            for p in expression.operands:
                if type(p).__name__ !=  'Constant':
                    allConstants=False
                    break
            if  allConstants:
                value = expression.value                
                return Constant(value,[],self.mgr)
        return expression             

    def getOperand(self):        
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

        if char.isalnum():    
            value=  self.getValue()
            if value=='if' and self.current == '(': 
                self.index+=1
                operand = self.getIfBlock()
            elif value=='while' and self.current == '(': 
                self.index+=1
                operand = self.getWhileBlock()            
            elif not self.end and self.current == '(':
                self.index+=1
                if '.' in value:
                    names = value.split('.')
                    name = names.pop()
                    variableName= '.'.join(names)
                    variable = Variable(variableName)
                    operand= self.getChildFunction(name,variable)
                else:
                    args=  self.getArgs(end=')')
                    operand= Function(value,args,self.mgr)                

            elif not self.end and self.current == '[':
                self.index+=1    
                operand = self.getIndexOperand(value)              
            elif self.mgr.reInt.match(value): 
                if isNegative:
                    value = int(value)* -1
                    isNegative= False 
                elif isBitNot:
                    value = ~ int(value)
                    isBitNot= False     
                else:
                    value =int(value)
                operand = Constant(value,[],self.mgr)
            elif self.mgr.reFloat.match(value):
                if isNegative:
                    value = float(value)* -1
                    isNegative= False
                elif isBitNot:
                    value = ~float(value)
                    isBitNot= False      
                else:
                    value =float(value)
                operand = Constant(value,[],self.mgr)
            elif value=='true':                
                operand = Constant(True,[],self.mgr)
            elif value=='false':                
                operand = Constant(False,[],self.mgr)
            elif self.mgr.isEnum(value):                
                operand= self.getEnum(value)
            else:
                operand = Variable(value)
        elif char == '\'' or char == '"':
            self.index+=1
            result=  self.getString(char)
            operand= Constant(result,[],self.mgr)
        elif char == '(':
            self.index+=1
            operand=  self.getExpression(_break=')') 
        elif char == '{':
            self.index+=1
            operand = self.getObject()  
        elif char == '[':
            self.index+=1
            elements=  self.getArgs(end=']')
            operand = Array('array',elements)

        if not self.end and  self.current=='.':
            self.index+=1
            name=  self.getValue()
            if self.current == '(': self.index+=1
            operand =self.getChildFunction(name,operand)

            # function= self.getOperand()
            # function.operands.insert(0,operand)
            # if '.' not in function.name :function.name = '.'+function.name
            # operand=function

        if isNegative:operand=self.mgr.newOperator('-',[operand])
        if isNot:operand=self.mgr.newOperator('!',[operand])
        if isBitNot:operand=self.mgr.newOperator('~',[operand])  
        return operand

    def priority(self,op:str,cardinality:int=2)->int:
        return self.mgr.priority(op,cardinality)        

    def getValue(self,increment:bool=True):
        buff=[]
        if increment:
            while not self.end and self.mgr.reAlphanumeric.match(self.current):
                buff.append(self.current)
                self.index+=1
        else:
            index = self.index
            while not self.end and self.mgr.reAlphanumeric.match(self.buffer[index]):
                buff.append(self.buffer[index])
                index+=1        
        return ''.join(buff)

    def getOperator(self):
        if self.end:return None 
        op=None
        if self.index+2 < self.length:
            triple = self.current+self.next+self.buffer[self.index+2]
            if triple in self.mgr.tripleOperators :op=triple
            # if triple in ['**=','//=','<<=','>>=']:op=triple
        if op is None and  self.index+1 < self.length:
            double = self.current+self.next
            if double in self.mgr.doubleOperators  :op=double
            # if double in ['**','//','>=','<=','!=','==','+=','-=','*=','/=','%=','&&','||','|=','^=','<<','>>']  :op=double
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
            else:raise ExpressionError('attribute '+name+' without value')
            value= self.getExpression(_break=',}')
            attribute = KeyValue(name,[value],self.mgr)
            attributes.append(attribute)
            if self.previous=='}':
                break
        
        return Object('object',attributes,self.mgr) 

    def getBlock(self):
        lines= []
        while True:
            line= self.getExpression(_break=';}')
            if line is not None :lines.append(line)
            if self.previous=='}':
                break        
        return Block('block',lines,self.mgr)     

    def getIfBlock(self):
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';') 

        nextValue=self.getValue(increment=False)
        elseblock=None
        if nextValue=='else':
            self.index+=len(nextValue)
            if  self.current == '{':
                self.index+=1  
                elseblock= self.getBlock()
            else:
                elseblock= self.getExpression(_break=';') 

        return If('if',[condition,block,elseblock],self.mgr) 

    def getWhileBlock(self):
        condition= self.getExpression(_break=')')
        if  self.current == '{':
            self.index+=1  
            block= self.getBlock()
        else:
            block= self.getExpression(_break=';') 

        return While('while',[condition,block],self.mgr)   

    def getChildFunction(self,name,parent):
        if name == 'foreach': return self.getForeach(parent)
        elif name == 'map': return self.getMap(parent)
        elif name == 'reverse': return self.getReverse(parent)
        elif name == 'first': return self.getFirst(parent)
        elif name == 'last': return self.getLast(parent)
        elif name == 'filter': return self.getFilter(parent)
        else: 
            args=  self.getArgs(end=')')
            args.insert(0,parent)
            return Function('.'+name,args,self.mgr)

        # if '.' in name:
        #     names = name.split('.')
        #     key = names.pop()
        #     variableName= '.'.join(names)
        #     variable = Variable(variableName)
        #     if key == 'foreach': return self.getForeach(variable)
        #     elif key == 'map': return self.getMap(variable)
        #     elif key == 'reverse': return self.getReverse(variable)
        #     elif key == 'first': return self.getFirst(variable)
        #     elif key == 'last': return self.getLast(variable)
        #     elif key == 'filter': return self.getFilter(variable)
        #     else: 
        #         args=  self.getArgs(end=')')
        #         args.insert(0,variable)
        #         return Function('.'+key,args)
        # else:
        #     args=  self.getArgs(end=')')
        #     return Function(name,args)

    def getForeach(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('foreach without body')
        body= self.getExpression(_break=')')
        return ArrayForeach(name,[variable,body],self.mgr) 

    def getMap(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('map without body')
        body= self.getExpression(_break=')')
        return ArrayMap(name,[variable,body],self.mgr)   

    def getReverse(self,variable): 
        if self.current == ')': self.index+=1       
        return ArrayReverse('',[variable],self.mgr) 
        # if self.current==':':self.index+=1
        # else:raise ExpressionError('reverse without body')
        # body= self.getExpression(_break=')')
        # return Reverse(name,[variable,body])   

    def getFirst(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('first without body')
        body= self.getExpression(_break=')')
        return ArrayFirst(name,[variable,body],self.mgr)  

    def getLast(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('last without body')
        body= self.getExpression(_break=')')
        return ArrayLast(name,[variable,body],self.mgr)                   

    def getFilter(self,variable):
        name= self.getValue()
        if self.current==':':self.index+=1
        else:raise ExpressionError('filter without body')
        body= self.getExpression(_break=')')
        return ArrayFilter(name,[variable,body],self.mgr)  

    def getIndexOperand(self,name):
        idx= self.getExpression(_break=']')
        operand= Variable(name)
        return BinaryOperator('[]',[operand,idx],self.mgr) 

    def getEnum(self,value):
        if '.' in value and self.mgr.isEnum(value):
            names = value.split('.')
            enumName = names[0]
            enumOption = names[1] 
            enumValue= self.mgr.getEnumValue(enumName,enumOption)
            # enumType = type(enumValue).__name__
            return Constant(enumValue,[],self.mgr)
        else:
            values= self.mgr.getEnum(value)
            attributes= []
            for name in values:
                _value = values[name]
                # _valueType = type(_value).__name__
                attribute = KeyValue(name,[Constant(_value)],[],self.mgr)
                attributes.append(attribute)
            return Object('object',attributes,self.mgr)
   

                            