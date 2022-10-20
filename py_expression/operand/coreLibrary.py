from typing import List
import time as t
import re
import math
import json
import dateutil.parser as dateParser
from datetime import date,datetime,time,timedelta
from os import path,getcwd
from py_expression.operand.operands import *
from py_expression.parser.model import Model
from py_expression.helper.helper import helper

class Volume():
    def __init__(self,_path):        
        self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
    def fullpath(self,_path):
        return path.join(self._root,_path)

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
        self.model.addOperator('+(a:T,b:T):T',self.Operators.addition,{'priority':4})
        self.model.addOperator('-(a:number,b:number):number',self.Operators.subtraction,{'priority':4})
        self.model.addOperator('-(a:number):number',self.Operators.negative,{'priority':8})
        self.model.addOperator('*(a:number,b:number):number',self.Operators.multiplication,{'priority':5})
        self.model.addOperator('/(a:number,b:number):number',self.Operators.division,{'priority':5})
        self.model.addOperator('**(a:number,b:number):number',self.Operators.exponentiation,{'priority':6})
        self.model.addOperator('//(a:number,b:number):number',self.Operators.floorDivision,{'priority':6})
        self.model.addOperator('%(a:number,b:number):number',self.Operators.mod,{'priority':7})        

        self.model.addOperator('&(a:number,b:number):number',self.Operators.bitAnd,{'priority':4})
        self.model.addOperator('|(a:number,b:number):number',self.Operators.bitOr,{'priority':4})
        self.model.addOperator('^(a:number,b:number):number',self.Operators.bitXor,{'priority':4})
        self.model.addOperator('~(a:number):number',self.Operators.bitNot ,{'priority':4})
        self.model.addOperator('<<(a:number,b:number):number',self.Operators.leftShift,{'priority':4})
        self.model.addOperator('>>(a:number,b:number):number',self.Operators.rightShift,{'priority':4})

        self.model.addOperator('==(a:T,b:T):boolean',self.Operators.equal,{'priority':3})
        self.model.addOperatorAlias('===', '==')
        self.model.addOperator('!=(a:T,b:T):boolean',self.Operators.notEqual,{'priority':3})
        self.model.addOperatorAlias('!==', '!=')
        self.model.addOperatorAlias('<>', '!=')
        self.model.addOperator('>(a:T,b:T):boolean',self.Operators.greaterThan,{'priority':3})
        self.model.addOperator('<(a:T,b:T):boolean',self.Operators.lessThan,{'priority':3})
        self.model.addOperator('>=(a:T,b:T):boolean',self.Operators.greaterThanOrEqual,{'priority':3})
        self.model.addOperator('<=(a:T,b:T):boolean',self.Operators.lessThanOrEqual,{'priority':3})

        self.model.addOperator('&&(a:T,b:T):boolean',self.And,{'priority':2})
        self.model.addOperator('||(a:T,b:T):boolean',self.Or,{'priority':2})
        self.model.addOperator('!(a:boolean):boolean',self.Operators._not,{'priority':4})

        self.model.addOperator('[](list:T[],index:integer):T',lambda a, b: a[b],{'priority':2})
        
        self.model.addOperator('=(a:T,b:T):T',self.Assignment,{'priority':1})
        self.model.addOperator('+=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.addition})
        self.model.addOperator('-=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.subtraction})
        self.model.addOperator('*=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.multiplication})
        self.model.addOperator('/=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.division})
        self.model.addOperator('**=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.exponentiation})
        self.model.addOperator('//=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.floorDivision})
        self.model.addOperator('%=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.mod})
        self.model.addOperator('&=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.bitAnd})
        self.model.addOperator('|=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.bitOr})
        self.model.addOperator('^=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.bitXor})
        self.model.addOperator('<<=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.leftShift})
        self.model.addOperator('>>=(a:number,b:number):number',self.Assignment,{'priority':1,'chained':self.Operators.rightShift})        

    def generalFunctions(self):
        self.model.addFunction('async sleep(ms: number)',self.General.sleep)
        self.model.addFunction('console(value:any)',self.General.console)   
    
    def nullFunctions(self):
        self.model.addFunction('nvl(a:T, b:T):T', self.Nullable.nvl)
        self.model.addFunction('nvl2(a:any, b:T,c:T):T',self.Nullable.nvl2)                 

    def comparisonFunctions(self):
        self.model.addFunction('isEmpty',self.Comparison.isEmpty)
        self.model.addFunction('between(value:any,from:any,to:any):boolean',self.Comparison.between)
        self.model.addFunction('includes(source:string|any[],value:any):boolean',self.Comparison.includes)
        self.model.addFunctionAlias('in', 'includes')
        self.model.addFunction('isNull(value:any):boolean', self.Comparison.isNull)
        self.model.addFunction('isNotNull(value:any):boolean', self.Comparison.isNotNull)
        self.model.addFunction('isEmpty(value:string):boolean', self.Comparison.isEmpty)
        self.model.addFunction('isNotEmpty(value:string):boolean',self.Comparison.isNotEmpty)
        self.model.addFunction('isBoolean(value:any):boolean', self.Comparison.isBoolean)
        self.model.addFunction('isNumber(value:any):boolean', self.Comparison.isNumber)
        self.model.addFunction('isInteger(value:any):boolean', self.Comparison.isInteger)
        self.model.addFunction('isDecimal(value:any):boolean', self.Comparison.isDecimal)
        self.model.addFunction('isString(value:any):boolean', self.Comparison.isString)
        self.model.addFunction('isDate(value:any):boolean', self.Comparison.isDate)
        self.model.addFunction('isDateTime(value:any):boolean', self.Comparison.isDateTime)
        self.model.addFunction('isTime(value:any):boolean', self.Comparison.isTime)
        self.model.addFunction('isObject(value:any):boolean', self.Comparison.isObject)
        self.model.addFunction('isArray(value:any):boolean', self.Comparison.isArray)
        self.model.addFunction('isBooleanFormat(value:string):boolean', self.Comparison.isBooleanFormat)
        self.model.addFunction('isNumberFormat(value:string):boolean', self.Comparison.isNumberFormat)
        self.model.addFunction('isIntegerFormat(value:string):boolean', self.Comparison.isIntegerFormat)
        self.model.addFunction('isDecimalFormat(value:string):boolean', self.Comparison.isDecimalFormat)
        self.model.addFunction('isDateFormat(value:string):boolean', self.Comparison.isDateFormat)
        self.model.addFunction('isDateTimeFormat(value:string):boolean', self.Comparison.isDateTimeFormat)
        self.model.addFunction('isTimeFormat(value:string):boolean', self.Comparison.isTimeFormat)

    def numberFunctions(self):
        self.model.addFunction('abs(x:number):number',self.Numbers.abs)
        self.model.addFunction('acos(x:number):number', self.Numbers.acos)
        self.model.addFunction('asin(x:number):number', self.Numbers.asin)
        self.model.addFunction('atan(x:number):number', self.Numbers.atan)
        self.model.addFunction('atan2(x:number):number',self.Numbers.atan2)
        self.model.addFunction('ceil(x:number):number', self.Numbers.ceil)
        self.model.addFunction('cos(x:number):number', self.Numbers.cos)
        self.model.addFunction('cosh(x:number):number', self.Numbers.cosh)
        self.model.addFunction('exp(x:number):number', self.Numbers.exp)
        self.model.addFunction('floor(x:number):number', self.Numbers.floor)
        self.model.addFunction('ln(x:number):number', self.Numbers.log)
        self.model.addFunction('log10(x:number):number', self.Numbers.log10)
        self.model.addFunction('log(x:number):number', self.Numbers.log)
        self.model.addFunction('remainder(n1:number,n2:number):number',self.Numbers.remainder)
        self.model.addFunction('round(num:number,decimals=0):number',self.Numbers.round)
        self.model.addFunction('sign(x:number):number',self.Numbers.sign)
        self.model.addFunction('sin(x:number):number', self.Numbers.sin)
        self.model.addFunction('sinh(x:number):number', self.Numbers.sinh)
        self.model.addFunction('tan(x:number):number', self.Numbers.tan)
        self.model.addFunction('tanh(x:number):number', self.Numbers.tanh)
        self.model.addFunction('trunc(x:number):number', self.Numbers.trunc)
    
    def conversionFunctions(self):
        self.model.addFunction('toString(value:any):string', self.Conversions.toString )
        self.model.addFunction('toNumber(value:any):number', self.Conversions.toNumber)
        self.model.addFunction('dateToString(date:date):string', self.Conversions.dateToString)
        self.model.addFunction('stringify(value:any):string', self.Conversions.stringify)
        self.model.addFunction('parse(value:string):any', self.Conversions.parse)
        self.model.addFunction('keys(obj: any):string[]', self.Conversions.keys)
        self.model.addFunction('values(obj: any):any[]',self.Conversions.values)
        self.model.addFunction('entries(obj: any):[string,any][]', self.Conversions.entries)
        self.model.addFunction('fromEntries(entries: [string,any][]): any', self.Conversions.fromEntries)
            
    def stringFunctions(self):        
        self.model.addFunction('chr(ascii: number):string',self.String.chr)
        self.model.addFunction('capitalize(value:string):string',self.String.capitalize)
        self.model.addFunction('endsWith(value:string, sub:string, start:number):boolean',self.String.endsWith)
        self.model.addFunction('strCount(source: string, value: string):number',self.String.strCount)
        self.model.addFunction('lower(value: string):string',self.String.lower) 
        self.model.addFunction('lpad(value: string, len: number, pad: string):string',self.String.lpad)
        self.model.addFunction('ltrim(value: string):string',self.String.ltrim)
        self.model.addFunction('indexOf(value:string, sub:string, start:number):number', self.String.indexOf)
        self.model.addFunction('join(values:string[],separator:string=","):string', self.String.join)
        self.model.addFunction('replace(value: string, source: string, target: string):string',self.String.replace)
        self.model.addFunction('rpad(value: string, len: number, pad: string):string',self.String.rpad)
        self.model.addFunction('rtrim(value: string):string',self.String.rtrim)
        self.model.addFunction('substring(value: string, from: number, count: number):string',self.String.substring)
        self.model.addFunctionAlias('substr', 'substring')
        self.model.addFunction('trim(value: string):string',self.String.trim)
        self.model.addFunction('upper(value: string):string',self.String.upper)
        self.model.addFunction('concat(...values:any):string',self.String.concat)
        self.model.addFunctionAlias('concatenate', 'concat')
        self.model.addFunction('test(value: any, regexp: string):boolean',self.String.test)
        self.model.addFunction('title(value:string):string',self.String.title)
        self.model.addFunction('match(value: string, regexp: string):any',self.String.match)
        self.model.addFunction('mask(value: string):string',self.String.mask)
        self.model.addFunction('split(value:string,separator:string=","):string[]', self.String.split)
        self.model.addFunction('startWith(value:string, sub:string, start:number):boolean',self.String.startswith)    
    
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
        self.model.addFunction('length(source: any[]|string):number', self.Array.length)
        self.model.addFunctionAlias('len', 'length')
        self.model.addFunction('slice(list: T[], from:integer, to:integer):T[]', self.Array.slice)
        self.model.addFunction('page(list: T[], page:integer, records:integer):T[]', self.Array.page)        

    def groupFunctions(self):
        self.model.addFunction('first(list: T[], predicate: boolean): T',self.First)
        self.model.addFunction('last(list: T[], predicate: boolean): T',self.Last)
           
    def signalFunctions(self):
        self.model.addFunction('listen(signals:string[],timeout:time):string',self.Listen )
        self.model.addFunction('wait(ms:time)',self.Wait) 
    
    def ioFunctions(self):
        self.model.addFunction('Volume(path:string):Volume',self.IO.Volume)
        self.model.addFunction('pathRoot():string',self.IO.pathRoot)
        self.model.addFunction('pathJoin(paths:string[]):string',self.IO.pathJoin)    
    
    class General():
        @staticmethod
        def sleep(secs:float=1000): 
            return t.sleep(secs)
        @staticmethod
        def console(value): 
            print(value)        
    class Nullable():
        @staticmethod
        def nvl(a:any,b:any)->any: 
            return a if a!=None and a!="" else b 
        def nvl2(a:any,b:any,c:any)->any: 
            return  b if a!=None and a!="" else c    
    class Comparison():
        @staticmethod
        def between(value:any,start:any,to:any)->bool:
            return helper.validator.between(value,start,to)
        @staticmethod
        def includes(source:any,value:any)->bool:
            return helper.validator.includes(source,value)
        @staticmethod
        def isNull(value:any)->bool:
            return helper.validator.isNull(value)
        @staticmethod
        def isNotNull(value:any)->bool:
            return helper.validator.isNotNull(value)
        @staticmethod
        def isEmpty(value:str)->bool:
            return helper.validator.isEmpty(value)
        @staticmethod
        def isNotEmpty(value:str)->bool:
            return helper.validator.isNotEmpty(value)
        @staticmethod
        def isBoolean(value:any)->bool:
            return helper.validator.isBoolean(value)
        @staticmethod
        def isNumber(value:any)->bool:
            return helper.validator.isNumber(value)
        @staticmethod
        def isInteger(value:any)->bool:
            return helper.validator.isInteger(value)
        @staticmethod
        def isDecimal(value:any)->bool:
            return helper.validator.isDecimal(value)
        @staticmethod
        def isString(value:any)->bool:
            return helper.validator.isString(value)
        @staticmethod
        def isDate(value:any)->bool:
            return helper.validator.isDate(value)
        @staticmethod
        def isDateTime(value:any)->bool:
            return helper.validator.isDateTime(value)
        @staticmethod
        def isTime(value:any)->bool:
            return helper.validator.isTime(value)
        @staticmethod
        def isObject(value:any)->bool:
            return helper.validator.isObject(value)
        @staticmethod
        def isArray(value:any)->bool:
            return helper.validator.isArray(value)
        @staticmethod
        def isBooleanFormat(value:str)->bool:
            return helper.validator.isBooleanFormat(value)
        @staticmethod
        def isNumberFormat(value:str)->bool:
            return helper.validator.isNumberFormat(value)
        @staticmethod
        def isIntegerFormat(value:str)->bool:
            return helper.validator.isIntegerFormat(value)
        @staticmethod
        def isDecimalFormat(value:str)->bool:
            return helper.validator.isDecimalFormat(value)
        @staticmethod
        def isDateFormat(value:str)->bool:
            return helper.validator.isDateFormat(value)
        @staticmethod
        def isDateTimeFormat(value:str)->bool:
            return helper.validator.isDateTimeFormat(value)
        @staticmethod
        def isTimeFormat(value:str)->bool:
            return helper.validator.isTimeFormat(value)
                 
    class Operators():
        @staticmethod
        def addition(a:any,b:any)->any:
            return a+b 
        @staticmethod
        def subtraction(a:float,b:float)->float:
            return a-b   
        @staticmethod
        def multiplication(a:float,b:float)->float:
            return a*b 
        @staticmethod
        def division(a:float,b:float)->float:
            return a/b  
        @staticmethod
        def exponentiation(a:float,b:float)->float:
            return a**b 
        @staticmethod
        def floorDivision(a:float,b:float)->float:
            return a//b   
        @staticmethod
        def mod(a:float,b:float)->float:
            return a%b 
        @staticmethod
        def negative(a:float)->float:
            return a *-1


        @staticmethod
        def bitAnd(a:float,b:float)->float:
            return a & b 
        @staticmethod
        def bitOr(a:float,b:float)->float:
            return a | b
        @staticmethod
        def bitXor(a:float,b:float)->float:
            return a ^ b                  
        @staticmethod
        def bitNot(a:float)->float:
            return ~ a
        @staticmethod
        def leftShift(a:float,b:float)->float:
            return a << b   
        @staticmethod
        def rightShift(a:float,b:float)->float:
            return a >> b   

        @staticmethod
        def equal(a:any,b:any)->bool:
            return a==b
        @staticmethod
        def notEqual(a:any,b:any)->bool:
            return a!=b          
        @staticmethod
        def greaterThan(a:any,b:any)->bool:
            return a>b
        @staticmethod
        def lessThan(a:any,b:any)->bool:
            return a<b 
        @staticmethod
        def greaterThanOrEqual(a:any,b:any)->bool:
            return a>=b
        @staticmethod
        def lessThanOrEqual(a:any,b:any)->bool:
            return a<=b               

        @staticmethod
        def _not(a:bool)->bool:
            return not a

        @staticmethod
        def assignment(a:any,b:any)->any: pass       

        @staticmethod
        def item(list:list[any],index:int):
            return list[index]   
    class Numbers():
        
        def remainder(n1:float,n2:float) -> float:
            return n1 % n2
        
        def round(num:float,decimals:float=0)-> float:
            return round(num,decimals)
        
        def sign(x: float) -> float:
            return (x > 0) - (x < 0)
        
        def abs(x: float) -> float:
            return abs(x)    
        
        @staticmethod
        def ceil(x: float) -> int:
            """
            Return the ceiling of x as an Integral.
            This is the smallest integer >= x.
            """    
            return math.ceil(x)
        @staticmethod    
        def copysign(x: float, y: float) -> float:
            """
            Return a float with the magnitude (absolute value) of x but the sign of y.
            On platforms that support signed zeros, copysign(1.0, -0.0)
            returns -1.0.
            """
            return math.copysign(x,y)
        @staticmethod    
        def factorial(x: int) -> int:
            """
            Find x!.
            Raise a ValueError if x is negative or non-integral.
            """
            return math.factorial(x)
        @staticmethod    
        def floor(x: float) -> int:
            """
            Return the floor of x as an Integral.
            This is the largest integer <= x.
            """
            return math.floor(x)
        @staticmethod    
        def fmod(x: float, y: float) -> float:
            """
            Return fmod(x, y), according to platform C.
            x % y may differ.
            """
            return math.fmod(x,y)
        @staticmethod        
        def frexp(x: float) -> tuple[float, int]:
            """
            Return the mantissa and exponent of x, as pair (m, e).
            m is a float and e is an int, such that x = m * 2.**e.
            If x is 0, m and e are both 0.  Else 0.5 <= abs(m) < 1.0.
            """
            return math.frexp(x)
        @staticmethod        
        def fsum(seq: list[float]) -> float:
            """
            Return an accurate floating point sum of values in the iterable seq.
            Assumes IEEE-754 floating point arithmetic.
            """
            return math.fsum(seq)
        @staticmethod       
        def isfinite(x:float)->bool:
            """Return True if x is neither an infinity nor a NaN, and False otherwise."""
            return math.isfinite(x)
        @staticmethod        
        def isnan(x:float)->bool:
            """Return True if x is a NaN (not a number), and False otherwise."""
            return math.isnan(x)
        @staticmethod        
        def ldexp(x:float,i:int)->float:
            """
            Return x * (2**i).
            This is essentially the inverse of frexp().
            """
            return math.ldexp(x,i) 
        @staticmethod        
        def modf(x:float)->tuple[float, float]:
            """
            Return the fractional and integer parts of x.
            Both results carry the sign of x and are floats.
            """
            return math.modf(x)
        @staticmethod         
        def trunc(x:float)->int:
            """
            Truncates the Real x to the nearest Integral toward 0.
            Uses the __trunc__ magic method.
            """
            return math.trunc(x)
        @staticmethod        
        def exp(x:float)->float:
            """Return e raised to the power of x."""
            return math.exp(x)
        @staticmethod         
        def expm1(x:float)->float:
            """
            Return exp(x)-1.
            This function avoids the loss of precision involved in the direct evaluation of exp(x)-1 for small x.
            """
            return math.expm1(x)
        @staticmethod     
        def log(x:float,base:float=None)->float:
            """
            log(x, [base=math.e])
            Return the logarithm of x to the given base.
            If the base not specified, returns the natural logarithm (base e) of x.
            """
            return math.log(x,base)
        @staticmethod         
        def log1p(x:float)->float:
            """
            Return the natural logarithm of 1+x (base e).
            The result is computed in a way which is accurate for x near zero.
            """
            return math.log1p(x)
        @staticmethod         
        def log2(x:float)->float:
            """Return the base 2 logarithm of x."""
            return math.log2(x)
        @staticmethod         
        def log10(x:float)->float:
            """Return the base 10 logarithm of x."""
            return math.log10(x)
        @staticmethod        
        def pow(x:float,y:float)->float:
            """Return x**y (x to the power of y)."""
            return math.pow(x,y)
        @staticmethod         
        def sqrt(x:float)->float:
            """Return the square root of x."""
            return math.sqrt(x)
        @staticmethod          
        def acos(x:float)->float:
            """
            Return the arc cosine (measured in radians) of x.
            The result is between 0 and pi.
            """
            return math.acos(x) 
        @staticmethod        
        def asin(x:float)->float:
            """
            Return the arc sine (measured in radians) of x.
            The result is between -pi/2 and pi/2.
            """
            return math.asin(x)
        @staticmethod        
        def atan(x:float)->float:
            """
            Return the arc tangent (measured in radians) of x.
            The result is between -pi/2 and pi/2.
            """
            return math.atan(x) 
        @staticmethod         
        def atan2(y:float,x:float)->float:
            """
            Return the arc tangent (measured in radians) of y/x.
            Unlike atan(y/x), the signs of both x and y are considered.
            """
            return math.atan2(y,x)
        @staticmethod      
        def cos(x:float)->float:
            """Return the cosine of x (measured in radians)."""
            return math.cos(x)
        @staticmethod     
        def hypot(x:list[float])->float:
            """
            hypot(*coordinates) -> value
            Multidimensional Euclidean distance from the origin to a point.
            Roughly equivalent to:
                sqrt(sum(x**2 for x in coordinates))
            For a two dimensional point (x, y), gives the hypotenuse
            using the Pythagorean theorem:  sqrt(x*x + y*y).
            For example, the hypotenuse of a 3/4/5 right triangle is:
            hypot(3.0, 4.0)
                5.0
            """
            return math.hypot(x) 
        @staticmethod    
        def sin(x:float)->float:
            """Return the sine of x (measured in radians)."""
            return math.sin(x)
        @staticmethod     
        def tan(x:float)->float:
            """Return the tangent of x (measured in radians)."""
            return math.tan(x)
        @staticmethod      
        def degrees(x:float)->float:
            """Convert angle x from radians to degrees."""
            return math.degrees(x)
        @staticmethod          
        def radians(x:float)->float:
            """Convert angle x from degrees to radians."""
            return math.radians(x)
        @staticmethod        
        def acosh(x:float)->float:
            """Return the inverse hyperbolic cosine of x."""
            return math.acosh(x)
        @staticmethod        
        def asinh(x:float)->float:
            """Return the inverse hyperbolic sine of x."""
            return math.asinh(x) 
        @staticmethod      
        def atanh(x:float)->float:
            """Return the inverse hyperbolic tangent of x."""
            return math.atanh(x)
        @staticmethod       
        def cosh(x:float)->float:
            """Return the hyperbolic cosine of x."""
            return math.cosh(x)
        @staticmethod        
        def sinh(x:float)->float:
            """Return the hyperbolic sine of x."""
            return math.sinh(x) 
        @staticmethod     
        def tanh(x:float)->float:
            """Return the hyperbolic tangent of x."""
            return math.tanh(x)
        @staticmethod         
        def erf(x:float)->float:
            """Error function at x."""
            return math.erf(x)
        @staticmethod         
        def erfc(x:float)->float:
            """Complementary error function at x."""
            return math.erfc(x)
        @staticmethod        
        def gamma(x:float)->float:
            """Gamma function at x."""
            return math.gamma(x)
        @staticmethod           
        def lgamma(x:float)->float:
            """Natural logarithm of absolute value of Gamma function at x."""
            return math.lgamma(x) 
        @staticmethod           
        def pi()->float:
            return math.pi
        @staticmethod           
        def e()->float:
            return math.e
    class Conversions():
        @staticmethod
        def toString(value:any)->str:
            return str(value)
        
        @staticmethod
        def toNumber(value:any)->float:
            return float(value)
        
        @staticmethod
        def dateToString(value:date)->str:
            return dateParser.parse(value).isoformat()
        
        @staticmethod
        def stringify(value:any)->str:
            return json.dumps(value, separators=(',', ':'))
        
        @staticmethod
        def parse(value:str)->dict:
            return json.loads(value)
        
        @staticmethod
        def keys(obj:dict)->any: #List<str>
            return obj.keys()
       
        @staticmethod
        def values(obj:dict)->any: #List<any>
            return obj.values()
        
        @staticmethod
        def entries(obj:dict)->any: #List<any>
            return obj.items()
        
        @staticmethod
        def fromEntries(entries:any)->dict: #List<any>
            return dict(entries)
    class String():
        # https://docs.python.org/2.5/lib/string-methods.html
        @staticmethod
        def chr(ascii:int)->str:               
            return chr(ascii)
        @staticmethod
        def capitalize(value:str)->str:
            """
            Return a capitalized version of the string.
            More specifically, make the first character have upper case and the rest lower case. 
            """    
            return value.capitalize()
        @staticmethod
        def concat(*args)->str: 
           return ''.join(args)        
        @staticmethod
        def endsWith(value:str,suffix:str,start: int = None, end: int = None) -> bool:
            """
            S.endswith(suffix[, start[, end]]) -> bool
            Return True if S ends with the specified suffix, False otherwise.
            With optional start, test S beginning at that position.
            With optional end, stop comparing S at that position.
            suffix can also be a tuple of strings to try.
            """ 
            return value.endswith(suffix,start,end)        
        @staticmethod
        def lower(value:str)->str: 
            """Return a copy of the string converted to lowercase."""
            return value.lower()        
        @staticmethod
        def lpad(value: str, len: int, pad: str)->str:
            """
            Return a left-justified string of length width.
            Padding is done using the specified fill character (default is a space).
            """             
            return value.ljust(len,pad)        
        @staticmethod
        def ltrim(value:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.
            If chars is given and not None, remove characters in chars instead.
            """
            return value.lstrip(chars)
        @staticmethod
        def indexOf(value:str,sub: str,start: int = None, end: int = None)->int:
            """
            S.find(sub[, start[, end]]) -> int
            Return the lowest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.
            Return -1 on failure.
            """ 
            return value.index(sub,start,end)
        @staticmethod
        def join(value:str,iterable: list[str])->bool: 
            """
            Concatenate any number of strings.
            The string whose method is called is inserted in between each given string.
            The result is returned as a new string.
            Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
            """
            return value.join(iterable)      
        @staticmethod
        def replace(value:str,old:str,new:str,count:int=None)->str: 
            """
            Return a copy with all occurrences of substring old replaced by new.
            count
                Maximum number of occurrences to replace.
                -1 (the default value) means replace all occurrences.
            If the optional argument count is given, only the first count occurrences are
            replaced.
            """
            return value.replace(old,new,count)
        @staticmethod
        def rpad(value: str, len: int, pad: str)->str:
            """
            Return a right-justified string of length width.
            Padding is done using the specified fill character (default is a space).
            """            
            return value.rjust(len,pad) 
        @staticmethod
        def rtrim(value:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.
            If chars is given and not None, remove characters in chars instead.
            """
            return value.rstrip(chars)        
        @staticmethod
        def substring(value:str,start: int, count: int)->str:            
            return value[start:start+count]
        @staticmethod
        def strCount(value:str,x: str,start: int = None, end: int = None)->int: 
            """
            S.count(sub[, start[, end]]) -> int
            Return the number of non-overlapping occurrences of substring sub in
            string S[start:end].  Optional arguments start and end are
            interpreted as in slice notation.
            """
            return value.count(x,start,end)
        @staticmethod
        def trim(value:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.
            If chars is given and not None, remove characters in chars instead.
            """
            return value.strip(chars)
        @staticmethod
        def upper(value:str)->str: 
            """Return a copy of the string converted to uppercase."""
            return value.upper()
        @staticmethod
        def test(value:str, regexp: str)->bool: 
            regExp= re.compile(regexp)
            return regExp.match(value) != None       
        @staticmethod
        def title(value:str)->str: 
            """
            Return a version of the string where each word is titleCased.
            More specifically, words start with upperCased characters and all remaining
            cased characters have lower case.
            """
            return value.title() 
        @staticmethod
        def match(value:str, regexp: str)->str: 
            regExp= re.compile(regexp)
            return regExp.match(value)
        def mask(value:str)->str: 
            if value==None:
                return value
            length = len(value)
            if length > 8:
                return value[0:3] + '*****' + value[length - 3, length]
            elif length > 5 :
                return value[0:1] + '*****' + value[length - 1, length]
            else:
                return '*' 
        @staticmethod
        def split(value:str,sep:str,maxSplit:int=None)->list[str]: 
            """
            Return a list of the words in the string, using sep as the delimiter string.
            sep
                The delimiter according which to split the string.
                None (the default value) means split according to any whitespace,
                and discard empty strings from the result.
            maxSplit
                Maximum number of splits to do.
                -1 (the default value) means no limit.
            """
            return value.split(sep,maxSplit)           
        @staticmethod
        def startswith(value:str,suffix:str,start: int = None, end: int = None) -> bool: 
            """
            S.startswith(prefix[, start[, end]]) -> bool
            Return True if S starts with the specified prefix, False otherwise.
            With optional start, test S beginning at that position.
            With optional end, stop comparing S at that position.
            prefix can also be a tuple of strings to try.
            """
            return value.startswith(suffix,start,end)       
        
        
        # Pending
        @staticmethod
        def encode(value:str,encoding: str = None, errors: str = None) -> bytes: 
            """
            Encode the string using the codec registered for encoding.
            encoding
                The encoding in which to encode the string.
            errors
                The error handling scheme to use for encoding errors.
                The default is 'strict' meaning that encoding errors raise a
                UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
                'xml char refer place' as well as any other name registered with
                codecs.register_error that can handle UnicodeEncodeErrors.
            """
            return value.encode(encoding,errors)      
        @staticmethod
        def isalnum(value:str)->bool: 
            """
            Return True if the string is an alpha-numeric string, False otherwise.
            A string is alpha-numeric if all characters in the string are alpha-numeric and
            there is at least one character in the string.
            """
            return value.isalnum()
        @staticmethod
        def isalpha(value:str)->bool: 
            """
            Return True if the string is an alphabetic string, False otherwise.
            A string is alphabetic if all characters in the string are alphabetic and there
            is at least one character in the string.
            """
            return value.isalpha()
        @staticmethod
        def isdigit(value:str)->bool: 
            """
            Return True if the string is a digit string, False otherwise.
            A string is a digit string if all characters in the string are digits and there
            is at least one character in the string.
            """
            return value.isdigit()
        @staticmethod
        def islower(value:str)->bool: 
            """
            Return True if the string is a lowercase string, False otherwise.
            A string is lowercase if all cased characters in the string are lowercase and
            there is at least one cased character in the string.
            """
            return value.islower()
        @staticmethod
        def isspace(value:str)->bool: 
            """
            Return True if the string is a whitespace string, False otherwise.
            A string is whitespace if all characters in the string are whitespace and there
            is at least one character in the string.
            """
            return value.isspace()
        @staticmethod
        def istitle(value:str)->bool: 
            """
            Return True if the string is a title-cased string, False otherwise.
            In a title-cased string, upper- and title-case characters may only
            follow uncased characters and lowercase characters only cased ones.
            """
            return value.istitle()
        @staticmethod
        def isupper(value:str)->bool: 
            """
            Return True if the string is an uppercase string, False otherwise.
            A string is uppercase if all cased characters in the string are uppercase and
            there is at least one cased character in the string.
            """
            return value.isupper()                
        @staticmethod
        def partition(value:str,sep:str)->tuple[str,str,str]: 
            """
            Partition the string into three parts using the given separator.
            This will search for the separator in the string.  If the separator is found,
            returns a 3-tuple containing the part before the separator, the separator
            itself, and the part after it.
            If the separator is not found, returns a 3-tuple containing the original string
            and two empty strings.
            """
            return value.partition(sep)        
        @staticmethod
        def rfind(value:str,sub: str,start: int = None, end: int = None)->int: 
            """
            S.rfind(sub[, start[, end]]) -> int
            Return the highest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.
            Return -1 on failure.
            """
            return value.rfind(sub,start,end)
        @staticmethod
        def rindex(value:str,sub: str,start: int = None, end: int = None)->int: 
            """
            S.rindex(sub[, start[, end]]) -> int
            Return the highest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.
            Raises ValueError when the substring is not found.
            """
            return value.rindex(sub,start,end)        
        @staticmethod
        def rpartition(value:str,sep:str)->tuple[str,str,str]: 
            """
            Partition the string into three parts using the given separator.
            This will search for the separator in the string, starting at the end. If
            the separator is found, returns a 3-tuple containing the part before the
            separator, the separator itself, and the part after it.
            If the separator is not found, returns a 3-tuple containing two empty strings
            and the original string.
            """
            return value.rpartition(sep)
        @staticmethod
        def rsplit(value:str,sep:str,maxSplit:int=None)->list[str]: 
            """
            Return a list of the words in the string, using sep as the delimiter string.
            sep
                The delimiter according which to split the string.
                None (the default value) means split according to any whitespace,
                and discard empty strings from the result.
            maxSplit
                Maximum number of splits to do.
                -1 (the default value) means no limit.
            Splits are done starting at the end of the string and working to the front.
            """
            return value.rsplit(sep,maxSplit)        
        @staticmethod
        def splitlines(value:str,keepEnds:bool=None)->list[str]: 
            """
            Return a list of the lines in the string, breaking at line boundaries.
            Line breaks are not included in the resulting list unless keepEnds is given and
            true.
            """
            return value.splitlines(keepEnds)        
        @staticmethod
        def swapcase(value:str)->str: 
            """Convert uppercase characters to lowercase and lowercase characters to uppercase."""
            return value.swapcase()               
        @staticmethod
        def zfill(value:str,width: int)->str: 
            """Pad a numeric string with zeros on the left, to fill a field of the given width."""
            return value.zfill(width)    
    class Date():
        # https://stackabuse.com/how-to-format-dates-in-python/
        # https://www.programiz.com/python-programming/datetime
        @staticmethod
        def strftime(self:date, fmt:str)->str:
            """format -> strftime() style string."""
            return datetime.strftime(self, fmt)
        @staticmethod
        def strptime(cls:datetime, date_string :str, forma:str)->datetime:
            """string, format -> new datetime parsed from a string (like time.strptime())."""
            return datetime.strptime(cls, date_string,forma) 
        @staticmethod
        def datetime(year:int, month:int=None, day:int=None, hour:int=0, minute:int=0, second:int=0,microsecond:int=0,tzinfo:t.timezone=None)->datetime:
            """
            datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])
            The year, month and day arguments are required. tzinfo may be None, or an     
            instance of a tzinfo subclass. The remaining arguments may be ints.
            """
            return datetime(year,month,day,hour,minute,second,microsecond,tzinfo)        
        @staticmethod
        def today()->date:
            """Current date or datetime:  same as self.__class__.fromtimestamp(time.time()). """
            return date.today()
        @staticmethod
        def now(tz:t.timezone=None)->datetime:
            """
            Returns new datetime object representing current time local to tz.
            tz
                Timezone object.
            If no tz is specified, uses local timezone.
            """
            return datetime.now(tz)         
        @staticmethod
        def date(year:int, month:int=None, day:int=None)->date:
            """date(year, month, day) --> date object"""
            return date(year,month,day) 
        @staticmethod
        def fromtimestamp(t:float)->date:
            """
            Create a date from a POSIX timestamp.
            The timestamp is a number, e.g. created via time.time(), that is interpreted
            as local time.
            """
            return date.fromtimestamp(t) 
        @staticmethod
        def time(hour:int=0, minute:int=0, second:int=0,microsecond:int=0,tzinfo:t.timezone=None)->time:
            """
            time([hour[, minute[, second[, microsecond[, tzinfo]]]]]) --> a time object
            All arguments are optional. tzinfo may be None, or an instance of
            a tzinfo subclass. The remaining arguments may be ints.
            """
            return time(hour,minute,second,microsecond,tzinfo) 
        #  self.addFunction('timedelta',timedelta)
        #  self.addFunction('timezone',pytz.timezone) 
    
    class Array():
        @staticmethod
        def pop(list:any)->any:
            return list.pop(1) 
        @staticmethod
        def length(source:any)->int:
            return len(source) 
        @staticmethod
        def slice(list:any,start:int,to:int)->any:
            return list[start:to]
        @staticmethod
        def page(list:any,page:int,records:int)->any:
            _from = (page - 1) * records
            if _from < 0:
                _from = 0			
            to = _from + records
            if to > len(list):
                to = len(list) - 1			
            return list[_from: to]    
        
    class IO():
        # https://docs.python.org/3/library/os.path.html

        @staticmethod
        def Volume(_path:str)->Volume:
            """create Volume"""
            return Volume(_path)

        @staticmethod
        def pathRoot()->str:
            """Return a unicode string representing the current working directory."""    
            return getcwd()

        @staticmethod
        def pathJoin(paths:list[str])->str:
            """
            Join one or more path components intelligently. 
            The return value is the concatenation of path and any members of *paths with exactly one directory separator following each non-empty part except the last, 
            meaning that the result will only end in a separator if the last part is empty. 
            If a component is an absolute path, all previous components are thrown away and joining continues from the absolute path component.
            """     
            return path.join(paths)    
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