import time as t
import math
import json
import dateutil.parser as dateParser
from datetime import date,datetime,time,timedelta
from os import path,getcwd
from py_expression.operand.operands import *
from py_expression.parser.model import Model

# class Volume():
#     def __init__(self,_path):        
#         self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
#     def fullpath(self,_path):
#         return path.join(self._root,_path)

class CoreLibrary(): 
    def __init__(self,model:Model):       
       self.model = model 

    def load(self):
       self.constants()
       self.enums()
       self.operators()
       self.generalFunctions()
       self.stringFunctions()
       self.numberFunctions()
       self.datetimeFunctions()
       self.ioFunctions()
       self.arrayFunctions()
       self.signalFunctions()   

    def constants(self):
        self.model.addConstant('true', True)
        self.model.addConstant('false', False)
        self.model.addConstant('null', None)
        
    def enums(self): 
        self.model.addEnum('DayOfWeek',{"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5,"Saturday":6,"Sunday":0}) 

    def formats(self):
        self.model.addFormat('email', '\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        self.model.addFormat('integer', '\d+$')
        self.model.addFormat('decimal', '\d+\.\d+$')
        self.model.addFormat('string', '[a-zA-Z0-9_.]+$')
        # https://stackoverflow.com/questions/3143070/javascript-regex-iso-datetime
        self.model.addFormat('date', '\d{4}-\d{2}-\d{2}$')
        self.model.addFormat('datetime', '\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)')
        self.model.addFormat('time', '\[0-2]\d:[0-5]\d:[0-5]\d')
   
    def operators(self):       

        self.model.addOperator('+(a:T,b:T):T',lambda a, b: a + b,{'priority':4})
        self.model.addOperator('-(a:number,b:number):number',lambda a, b: a - b,{'priority':4})
        self.model.addOperator('-(a:number):number',lambda a : a * -1,{'priority':8})
        self.model.addOperator('*(a:number,b:number):number',lambda a, b: a * b,{'priority':5})
        self.model.addOperator('/(a:number,b:number):number',lambda a, b: a / b,{'priority':5})
        self.model.addOperator('**(a:number,b:number):number',lambda a, b: a ** b,{'priority':6})
        self.model.addOperator('//(a:number,b:number):number',lambda a, b: a // b,{'priority':6})
        self.model.addOperator('%(a:number,b:number):number',lambda a, b: a % b,{'priority':7})        

        self.model.addOperator('&(a:number,b:number):number',lambda a, b: a & b,{'priority':4})
        self.model.addOperator('|(a:number,b:number):number',lambda a, b: a | b,{'priority':4})
        self.model.addOperator('^(a:number,b:number):number',lambda a, b: a ^ b,{'priority':4})
        self.model.addOperator('~(a:number):number',lambda a: ~a ,{'priority':4})
        self.model.addOperator('<<(a:number,b:number):number',lambda a, b: a << b,{'priority':4})
        self.model.addOperator('>>(a:number,b:number):number',lambda a, b: a >> b,{'priority':4})

        self.model.addOperator('==(a:T,b:T):boolean',lambda a, b: a == b,{'priority':3})
        self.model.addOperatorAlias('===', '==')
        self.model.addOperator('!=(a:T,b:T):boolean',lambda a, b: a != b,{'priority':3})
        self.model.addOperatorAlias('!==', '!=')
        self.model.addOperatorAlias('<>', '!=')
        self.model.addOperator('>(a:T,b:T):boolean',lambda a, b: a > b,{'priority':3})
        self.model.addOperator('<(a:T,b:T):boolean',lambda a, b: a <b,{'priority':3})
        self.model.addOperator('>=(a:T,b:T):boolean',lambda a, b: a >= b,{'priority':3})
        self.model.addOperator('<=(a:T,b:T):boolean',lambda a, b: a <= b,{'priority':3})

        self.model.addOperator('&&(a:T,b:T):boolean',lambda a, b: a and b,{'priority':2})
        self.model.addOperator('||(a:T,b:T):boolean',lambda a, b: a or b,{'priority':2})
        self.model.addOperator('!(a:boolean):boolean',lambda a: not a,{'priority':4})

        self.model.addOperator('[](list:T[],index:integer):T',lambda a, b: a[b],{'priority':2})
        
        self.model.addOperator('=(a:T,b:T):T',self.Assignment,{'priority':1})
        self.model.addOperator('+=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a + b})
        self.model.addOperator('-=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a - b})
        self.model.addOperator('*=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a * b})
        self.model.addOperator('/=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a / b})
        self.model.addOperator('**=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a ** b})
        self.model.addOperator('//=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a // b})
        self.model.addOperator('%=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a % b})
        self.model.addOperator('&=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a & b})
        self.model.addOperator('|=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a | b})
        self.model.addOperator('^=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a ^ b})
        self.model.addOperator('<<=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a << b})
        self.model.addOperator('>>=(a:number,b:number):number',self.Assignment,{'priority':1,'chainedFunction':lambda a, b: a >> b})        

    def generalFunctions(self):
        self.model.addFunction('async sleep(ms: number)',lambda ms: t.sleep(ms))
        self.model.addFunction('console(value:any)',lambda value: print(value) )   
    
    def nullFunctions(self):
        self.model.addFunction('nvl(a:T, b:T):T', lambda a,b: a if a!=None and a!="" else b )
        self.model.addFunction('nvl2(a:any, b:T,c:T):T',lambda a,b,c: b if a!=None and a!="" else c )                 

    def comparisonFunctions(self):        
        self.model.addFunction('isEmpty',lambda a:  a==None or a =="" )
        # self.model.addFunction('isalnum',self.String.isalnum)
        # self.model.addFunction('isalpha',self.String.isalpha)
        # self.model.addFunction('isdigit',self.String.isdigit)
        # self.model.addFunction('islower',self.String.islower)
        # self.model.addFunction('isspace',self.String.isspace)
        # self.model.addFunction('istitle',self.String.istitle)
        # self.model.addFunction('isupper',self.String.isupper)

    def numberFunctions(self):
        self.model.addFunction('abs(x:number):number',lambda x: abs(x))
        self.model.addFunction('acos(x:number):number', lambda x: math.acos(x))
        self.model.addFunction('asin(x:number):number', lambda x:math.asin(x))
        self.model.addFunction('atan(x:number):number', lambda x:math.atan(x))
        self.model.addFunction('atan2(x:number):number',lambda x:math.atan2(x))
        self.model.addFunction('ceil(x:number):number', lambda x:math.ceil(x))
        self.model.addFunction('cos(x:number):number', lambda x:math.cos(x))
        self.model.addFunction('cosh(x:number):number', lambda x:math.cosh(x))
        self.model.addFunction('exp(x:number):number', lambda x:math.exp(x))
        self.model.addFunction('floor(x:number):number', lambda x:math.floor(x))
        self.model.addFunction('ln(x:number):number', lambda x:math.log(x))
        self.model.addFunction('log10(x:number):number', lambda x:math.log10(x))
        self.model.addFunction('log(x:number):number', lambda x:math.log(x))
        self.model.addFunction('remainder(n1:number,n2:number):number',lambda n1,n2: n1 % n2)
        self.model.addFunction('round(num:number,decimals=0):number',lambda num,decimals=0: round(num,decimals))
        self.model.addFunction('sign(x:number):number',lambda x:  (x > 0) - (x < 0))
        self.model.addFunction('sin(x:number):number', lambda x:math.sin(x))
        self.model.addFunction('sinh(x:number):number', lambda x:math.sinh(x))
        self.model.addFunction('tan(x:number):number', lambda x:math.tan(x))
        self.model.addFunction('tanh(x:number):number', lambda x:math.tanh(x))
        self.model.addFunction('trunc(x:number):number', lambda x:math.trunc(x))
    
    def conversionFunctions(self):
        self.model.addFunction('toString(value:any):string', lambda value: str(value) )
        self.model.addFunction('toNumber(value:any):number', lambda value: float(value))
        self.model.addFunction('dateToString(date:date):string', lambda value: dateParser.parse(value).isoformat())
        self.model.addFunction('stringify(value:any):string', lambda value: json.dumps(value, separators=(',', ':')) )
        self.model.addFunction('parse(value:string):any', lambda value: json.loads(value))
        self.model.addFunction('keys(obj: any):string[]', lambda obj: obj.keys())
        self.model.addFunction('values(obj: any):any[]', lambda obj: obj.values())
        self.model.addFunction('entries(obj: any):[string,any][]', lambda obj: obj.items())
        self.model.addFunction('fromEntries(entries: [string,any][]): any', lambda entries: dict(entries))
            
    def stringFunctions(self):        
        self.model.addFunction('chr(ascii: number):string', lambda ascii: None )
        self.model.addFunction('capitalize(value:string):string',lambda value: str.capitalize(value))
        self.model.addFunction('endsWith(value:string, sub:string, start:number):boolean',lambda value,sub,start: str.endswith(value, sub, start))
        self.model.addFunction('strCount(source: string, value: string):number',lambda source,value:str.count(source,value))
        self.model.addFunction('lower(value: string):string',lambda value: str.lower(value)) 
        self.model.addFunction('lpad(value: string, len: number, pad: string):string', lambda str,len,pad: None )
        self.model.addFunction('ltrim(value: string):string',lambda value: str.lstrip(value))
        self.model.addFunction('replace(value: string, source: string, target: string):string',lambda value, source,target: str.replace(value,source,target))
        self.model.addFunction('rpad(value: string, len: number, pad: string):string',lambda str,len,pad: None)
        self.model.addFunction('rtrim(value: string):string',lambda value: str.rstrip(value))
        self.model.addFunction('substring(value: string, from: number, count: number):string',lambda str,_from,count: None)
        self.model.addFunctionAlias('substr', 'substring')
        self.model.addFunction('trim(value: string):string',lambda value: str.strip(value))
        self.model.addFunction('upper(value: string):string',lambda value: str.upper(value))
        self.model.addFunction('concat(...values:any):string',lambda values: None)
        self.model.addFunctionAlias('concatenate', 'concat')
        self.model.addFunction('test(value: any, regexp: string):boolean',lambda value,regexp: None)
        self.model.addFunction('title(value:string):string',lambda value: str.title(value))
        self.model.addFunction('match(value: string, regexp: string):any',lambda value,regexp: None)
        self.model.addFunction('mask(value: string):string',lambda value,regexp: None)
        self.model.addFunction('startWith(value:string, sub:string, start:number):boolean',lambda value,sub,start: str.startswith(value, sub, start))    
    
    def datetimeFunctions(self):
        # https://stackabuse.com/how-to-format-dates-in-python/
        # https://www.programiz.com/python-programming/datetime
        self.model.addFunction('strftime(date:dateTime,fmt:string)',lambda date,fmt: datetime.strftime(date, fmt))
        # self.model.addFunction('strptime',lambda cls,date_string,forma: datetime.strptime(cls, date_string,forma))        
        # self.model.addFunction('datetime',lambda year,month=None,day=None,hour=0,minute=0,second=0,microsecond=0,tzinfo=None: datetime(year,month,day,hour,minute,second,microsecond,tzinfo) )
        # self.model.addFunction('today',lambda : date.today())
        # self.model.addFunction('now(tz:any)',lambda tz=None: datetime.now(tz))
        # self.model.addFunction('date',lambda year,month=None,day=None: date(year,month,day))
        # self.model.addFunction('fromtimestamp',lambda t: date.fromtimestamp(t))
        # self.model.addFunction('time',lambda hour=0,minute=0,second=0,microsecond=0,tzinfo=None: time(hour,minute,second,microsecond,tzinfo))
    
    def arrayFunctions(self):
        self.model.addFunction('map(list: any[], predicate: T):T[]',self.Map)
        self.model.addFunctionAlias('select', 'map') 
        self.model.addFunction('foreach(list: any[], predicate: any)',self.Foreach)
        self.model.addFunctionAlias('each', 'foreach')        
        self.model.addFunction('filter(list: T[], predicate: boolean):T[]',self.Filter)
        self.model.addFunctionAlias('where', 'filter')
        self.model.addFunction('reverse(list: T[], predicate: any):T[]',self.Reverse)        
        self.model.addFunction('sort(list: T[], predicate: any):T[]',self.Sort)
        self.model.addFunctionAlias('order', 'sort')
        self.model.addFunction('remove(list: T[], predicate: boolean):T[]',self.Remove)
        self.model.addFunctionAlias('delete', 'remove')
        self.model.addFunction('push(list: T[], value: T):T[]',self.Push)
        self.model.addFunctionAlias('insert', 'push')
        self.model.addFunction('pop(list: T[]): T',self.Pop)
        # self.model.addFunction('length(source: any[]|string):number', None)
        # self.model.addFunctionAlias('len', 'length')
        # self.model.addFunction('slice(list: T[], from:integer, to:integer):T[]', None)
        # self.model.addFunction('page(list: T[], page:integer, records:integer):T[]', None)        

    def groupFunctions(self):
        self.model.addFunction('first(list: T[], predicate: boolean): T',self.First)
        self.model.addFunction('last(list: T[], predicate: boolean): T',self.Last)
           
    def signalFunctions(self):
        self.model.addFunction('listen(signals:string[],timeout:time):string',self.Listen )
        self.model.addFunction('wait(ms:time)',self.Wait) 
    
    def ioFunctions(self):
        pass 
    #     self.model.addFunction('Volume(path:string):Volume',lambda path: Volume(path))
    #     self.model.addFunction('pathRoot():string',lambda : getcwd())
    #     self.model.addFunction('pathJoin(paths:string[]):string',lambda paths: path.join(paths) )
    
    class And(Operator):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value
                if not value.value : return Value(False)
                values.append(value.value)                
            if len(values) == 1:
                return self._children[1].eval(token) 
    class Or(Operator):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value
                if value.value : return Value(True)
                values.append(value)                
            if len(values) == 1:
                return self._children[1].eval(token)
    class Assignment(Operator):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value  
                values.append(value.value)
            if len(values) ==1:
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)
                value = values[1] if self._function is None else self._function(values[0],values[1])
                self._children[0].set(value,token)
                return Value(value)
    class Foreach(ArrowFunction):   
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value
                values.append(value.value)
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value                    
                    values[1] = i
            return Value()        
    class Map(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                values.append(value.value)
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    values.append(value.value)
                    values[1] = i 
            return Value(values[2:])  
    class First(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value  
                values.append(value.value)
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    if value.value: return Value(p)                    
            return Value(None)
    class Last(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                value.value.reverse() 
                values.append(value.value)
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    if value.value: return Value(p)                    
            return Value(None)      
    class Filter(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                values.append(value.value)
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    if value.value: values.append(p) 
                    values[1] = i                   
            return Value(values[2:])       
    class Reverse(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                value.value.reverse() 
                values.append(value.value)

            if len(self._children)==1:
                return Value(values[0])   
            
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    values.append({'ord':value.value,'p':p}) 
                    values[1] = i

            result = values[2:]  
            result.sort((lambda p: p['ord']))
            result.reverse()    
            return Value(map(lambda p: p['p'],result))                                  
    class Sort(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                values.append(value.value)

            if len(self._children)==1:
                return Value(values[0])   
            
            values.append(0)    
            for i,p in enumerate(values[0]):
                if i>=values[1]:
                    self._children[1].set(p,token)
                    value = self._children[2].eval(token)
                    if token.isBreak: return value
                    values.append({'ord':value.value,'p':p}) 
                    values[1] = i

            result = values[2:]  
            result.sort((lambda p: p['ord']))
            return Value(map(lambda p: p['p'],result))           
    class Push(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value 
                values.append(value.value)
            if len(values) == 1:
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)

            values[0].append(values[1])
            return Value(values[0])
    class Pop(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value
                values.append(value.value)
            if len(values) == 1:   
                if len(self._children)>1:
                    value = self._children[1].eval(token)
                    if token.isBreak: return value
                    values.append(value.value)
                else:
                    index = len(self._children) -1 
                    values.append(index)

            return Value(values[0].pop(values[1]))   
    class Remove(ArrowFunction):
        def solve(self,values,token:Token)->Value:
            if len(values) == 0:
                value = self._children[0].eval(token)
                if token.isBreak: return value
                values.append(value.value)
            if len(values) == 1: 
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)
            return Value(values[0].remove(values[1]) )             
    class Wait(FunctionRef):
        def solve(self,values,token:Token)->Value:
            key = 'wait:'+token.id
            if len(values) == 0: 
                value = self._children[0].eval(token)
                if token.isBreak: return value
                values.append(value.value) 
                signal = Signal(key,values[0])
                token.addListener(signal)
                return Value()
            else:
                if key in token.signals:
                    token.clearListeners()
                return Value() 
    class Listen(FunctionRef):
        def solve(self,values,token:Token)->Value:
            timeKey = 'time:'+token.id
            if len(values) == 0:                                    
                value = self._children[0].eval(token)
                if token.isBreak: return value
                values.append(value.value)
                for key in values[0]:     
                    signal = Signal(key)
                    token.addListener(signal) 
                if len(self._children)== 1:
                    return Value()      
            if len(self._children)== 2 and len(values) == 1:
                value = self._children[1].eval(token)
                if token.isBreak: return value
                values.append(value.value)
                signal = Signal(timeKey,values[1])
                token.addListener(signal)
                return Value()                     
            else:
                for key in values[0]: 
                    if key in token.signals:
                        token.clearListeners()
                        return Value(key)
                if timeKey in token.signals:
                    token.clearListeners()
                    return Value('time')
                return Value()  
   
                