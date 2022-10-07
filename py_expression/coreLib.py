import time as t
import math
from datetime import date,datetime,time,timedelta
from os import path,getcwd
from .base import *
from .model import Model

class Volume():
    def __init__(self,_path):        
        self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
    def fullpath(self,_path):
        return path.join(self._root,_path)

class CoreLib(): 
    def __init__(self,model:Model):       
       self.model = model 

    def load(self):
       self.initEnums()
       self.initOperators()
       self.generalFunctions()
       self.stringFunctions()
       self.mathFunctions()
       self.datetimeFunctions()
       self.ioFunctions()
       self.arrayFunctions()
       self.signalFunctions()   

    def initEnums(self): 
        self.model.addEnum('DayOfWeek',{"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5,"Saturday":6,"Sunday":0}) 

    def initOperators(self):       

        self.model.addOperator('+','arithmetic',self.Operators.addition,4)
        self.model.addOperator('-','arithmetic',self.Operators.subtraction,4)
        self.model.addOperator('-','arithmetic',self.Operators.negative,8)
        self.model.addOperator('*','arithmetic',self.Operators.multiplication,5)
        self.model.addOperator('/','arithmetic',self.Operators.division,5)
        self.model.addOperator('**','arithmetic',self.Operators.exponentiation,6)
        self.model.addOperator('//','arithmetic',self.Operators.floorDivision,6)
        self.model.addOperator('%','arithmetic',self.Operators.mod,7)
        

        self.model.addOperator('&','bitwise',self.Operators.bitAnd,4)
        self.model.addOperator('|','bitwise',self.Operators.bitOr,4)
        self.model.addOperator('^','bitwise',self.Operators.bitXor,4)
        self.model.addOperator('~','bitwise',self.Operators.bitNot,4)
        self.model.addOperator('<<','bitwise',self.Operators.leftShift,4)
        self.model.addOperator('>>','bitwise',self.Operators.rightShift,4)

        self.model.addOperator('==','comparison',self.Operators.equal,3)
        self.model.addOperator('!=','comparison',self.Operators.notEqual,3)
        self.model.addOperator('>','comparison',self.Operators.greaterThan,3)
        self.model.addOperator('<','comparison',self.Operators.lessThan,3)
        self.model.addOperator('>=','comparison',self.Operators.greaterThanOrEqual,3)
        self.model.addOperator('<=','comparison',self.Operators.lessThanOrEqual,3)

        self.model.addOperator('&&','logical',self.Operators._and,2,self.Operators.And)
        self.model.addOperator('||','logical',self.Operators._or,2,self.Operators.Or)
        self.model.addOperator('!','logical',self.Operators._not,4)

        self.model.addOperator('[]','list',self.Operators.item)
        
        self.model.addOperator('=','assignment',self.Operators.assignment,1,self.Operators.Assignment)
        self.model.addOperator('+=','assignment',self.Operators.assignmentAddition,1,self.Operators.Assignment,self.Operators.addition)
        self.model.addOperator('-=','assignment',self.Operators.assignmentSubtraction,1,self.Operators.Assignment,self.Operators.subtraction)
        self.model.addOperator('*=','assignment',self.Operators.assignmentMultiplication,1,self.Operators.Assignment,self.Operators.multiplication)
        self.model.addOperator('/=','assignment',self.Operators.assignmentDivision,1,self.Operators.Assignment,self.Operators.division)
        self.model.addOperator('**=','assignment',self.Operators.assignmentExponentiation,1,self.Operators.Assignment,self.Operators.exponentiation)
        self.model.addOperator('//=','assignment',self.Operators.assignmentFloorDivision,1,self.Operators.Assignment,self.Operators.floorDivision)
        self.model.addOperator('%=','assignment',self.Operators.assignmentMod,1,self.Operators.Assignment,self.Operators.mod)
        self.model.addOperator('&=','assignment',self.Operators.assignmentBitAnd,1,self.Operators.Assignment,self.Operators.bitAnd)
        self.model.addOperator('|=','assignment',self.Operators.assignmentBitOr,1,self.Operators.Assignment,self.Operators.bitOr)
        self.model.addOperator('^=','assignment',self.Operators.assignmentBitXor,1,self.Operators.Assignment,self.Operators.bitXor)
        self.model.addOperator('<<=','assignment',self.Operators.assignmentLeftShift,1,self.Operators.Assignment,self.Operators.leftShift)
        self.model.addOperator('>>=','assignment',self.Operators.assignmentRightShift,1,self.Operators.Assignment,self.Operators.rightShift)        

    def generalFunctions(self):
        self.model.addFunction('nvl',self.General.nvl )
        self.model.addFunction('isEmpty',self.General.isEmpty)
        self.model.addFunction('sleep',self.General.sleep)        

    def stringFunctions(self):
        self.model.addFunction('capitalize',self.String.capitalize)
        self.model.addFunction('strCount',self.String.count)
        self.model.addFunction('encode',self.String.encode)
        self.model.addFunction('endswith',self.String.endswith)
        self.model.addFunction('find',self.String.find)
        self.model.addFunction('index',self.String.index)
        self.model.addFunction('isalnum',self.String.isalnum)
        self.model.addFunction('isalpha',self.String.isalpha)
        self.model.addFunction('isdigit',self.String.isdigit)
        self.model.addFunction('islower',self.String.islower)
        self.model.addFunction('isspace',self.String.isspace)
        self.model.addFunction('istitle',self.String.istitle)
        self.model.addFunction('isupper',self.String.isupper)
        self.model.addFunction('strJoin',self.String.join)
        self.model.addFunction('ljust',self.String.ljust)
        self.model.addFunction('lower',self.String.lower)
        self.model.addFunction('lstrip',self.String.lstrip)
        self.model.addFunction('strPartition',self.String.partition)
        self.model.addFunction('replace',self.String.replace)
        self.model.addFunction('rfind',self.String.rfind)
        self.model.addFunction('rindex',self.String.rindex)
        self.model.addFunction('rjust',self.String.rjust)
        self.model.addFunction('rpartition',self.String.rpartition)
        self.model.addFunction('rsplit',self.String.rsplit)
        self.model.addFunction('rstrip',self.String.lstrip)
        self.model.addFunction('split',self.String.split)
        self.model.addFunction('splitlines',self.String.splitlines)
        self.model.addFunction('startswith',self.String.startswith)
        self.model.addFunction('strip',self.String.lstrip)
        self.model.addFunction('swapcase',self.String.swapcase)
        self.model.addFunction('title',self.String.title)
        # self.model.addFunction('translate',self.String.translate)
        self.model.addFunction('upper',self.String.upper)
        self.model.addFunction('zfill',self.String.zfill)   

    def mathFunctions(self):
        self.model.addFunction('ceil',self.Math.ceil)
        self.model.addFunction('copysign',self.Math.copysign) 
        self.model.addFunction('factorial',self.Math.factorial) 
        self.model.addFunction('floor',self.Math.floor) 
        self.model.addFunction('fmod',self.Math.fmod) 
        self.model.addFunction('frexp',self.Math.frexp) 
        self.model.addFunction('fsum',self.Math.fsum) 
        self.model.addFunction('isfinite',self.Math.isfinite) 
        self.model.addFunction('isnan',self.Math.isnan) 
        self.model.addFunction('ldexp',self.Math.ldexp) 
        self.model.addFunction('modf',self.Math.modf) 
        self.model.addFunction('trunc',self.Math.trunc) 
        self.model.addFunction('exp',self.Math.exp) 
        self.model.addFunction('expm1',self.Math.expm1) 
        self.model.addFunction('log',self.Math.log) 
        self.model.addFunction('log1p',self.Math.log1p) 
        self.model.addFunction('log2',self.Math.log2) 
        self.model.addFunction('log10',self.Math.log10) 
        self.model.addFunction('pow',self.Math.pow) 
        self.model.addFunction('sqrt',self.Math.sqrt) 
        self.model.addFunction('acos',self.Math.acos) 
        self.model.addFunction('asin',self.Math.asin) 
        self.model.addFunction('atan',self.Math.atan) 
        self.model.addFunction('atan2',self.Math.atan2) 
        self.model.addFunction('cos',self.Math.cos) 
        self.model.addFunction('hypot',self.Math.hypot) 
        self.model.addFunction('sin',self.Math.sin) 
        self.model.addFunction('tan',self.Math.tan) 
        self.model.addFunction('degrees',self.Math.degrees)
        self.model.addFunction('radians',self.Math.radians)
        self.model.addFunction('acosh',self.Math.acosh)
        self.model.addFunction('asinh',self.Math.asinh)
        self.model.addFunction('atanh',self.Math.atanh)
        self.model.addFunction('cosh',self.Math.cosh)
        self.model.addFunction('sinh',self.Math.sinh)
        self.model.addFunction('tanh',self.Math.tanh)
        self.model.addFunction('erf',self.Math.erf)
        self.model.addFunction('erfc',self.Math.erfc)
        self.model.addFunction('gamma',self.Math.gamma)
        self.model.addFunction('lgamma',self.Math.lgamma)
        self.model.addFunction('pi',self.Math.pi)
        self.model.addFunction('e',self.Math.e)
    
    def datetimeFunctions(self):
        self.model.addFunction('strftime',self.Date.strftime)
        self.model.addFunction('strptime',self.Date.strptime)        
        self.model.addFunction('datetime',self.Date.datetime)
        self.model.addFunction('today',self.Date.today)
        self.model.addFunction('now',self.Date.now)
        self.model.addFunction('date',self.Date.date)
        self.model.addFunction('fromtimestamp',self.Date.fromtimestamp)
        self.model.addFunction('time',self.Date.time)
    
    def ioFunctions(self): 
        self.model.addFunction('Volume',self.IO.Volume)
        self.model.addFunction('pathRoot',self.IO.pathRoot)
        self.model.addFunction('pathJoin',self.IO.pathJoin)

    def arrayFunctions(self): 
        self.model.addFunction('foreach',self.Array.foreach,self.Array.ArrayForeach,True)
        self.model.addFunction('map',self.Array.map,self.Array.ArrayMap,True)
        self.model.addFunction('filter',self.Array.filter,self.Array.ArrayFilter,True)
        self.model.addFunction('reverse',self.Array.reverse,self.Array.ArrayReverse,True)
        self.model.addFunction('first',self.Array.first,self.Array.ArrayFirst,True)
        self.model.addFunction('last',self.Array.last,self.Array.ArrayLast,True)
        self.model.addFunction('sort',self.Array.sort,self.Array.ArraySort,True)
        self.model.addFunction('push',self.Array.push,self.Array.ArrayPush)
        self.model.addFunction('pop',self.Array.pop,self.Array.ArrayPop)
        self.model.addFunction('remove',self.Array.remove,self.Array.ArrayRemove)

    def signalFunctions(self):
        self.model.addFunction('listen',self.Signal.listen,self.Signal.Listen )
        self.model.addFunction('wait',self.Signal.wait,self.Signal.Wait)
        self.model.addFunction('listeners',self.Signal.listen,self.Signal.Listeners )

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
        def _and(a:bool,b:bool)->bool:
            return a and b
        @staticmethod
        def _or(a:bool,b:bool)->bool:
            return a or b  

        @staticmethod
        def assignment(a:any,b:any)->any: pass
        @staticmethod
        def assignmentAddition(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentSubtraction(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentMultiplication(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentDivision(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentExponentiation(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentFloorDivision(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentMod(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentBitAnd(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentBitOr(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentBitXor(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentLeftShift(a:float,b:float)->float: pass 
        @staticmethod
        def assignmentRightShift(a:float,b:float)->float: pass 

        @staticmethod
        def item(list:list[any],index:int):
            return list[index]

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
  
    class General():
        @staticmethod
        def nvl(a:any,b:any)->any: 
            return a if a!=None and a!="" else b 
        @staticmethod
        def isEmpty(a:any)->bool:return  a==None or a =="" 
        @staticmethod
        def sleep(secs:float=1000): 
            return t.sleep(secs)
       
    class String():
        # https://docs.python.org/2.5/lib/string-methods.html
        @staticmethod
        def capitalize(self:str)->str:
            """
            Return a capitalized version of the string.
            More specifically, make the first character have upper case and the rest lower case. 
            """    
            return str.capitalize(self)
        @staticmethod
        def count(self:str,x: str,start: int = None, end: int = None)->int: 
            """
            S.count(sub[, start[, end]]) -> int

            Return the number of non-overlapping occurrences of substring sub in
            string S[start:end].  Optional arguments start and end are
            interpreted as in slice notation.
            """
            return str.count(self,x,start,end)
        @staticmethod
        def encode(self:str,encoding: str = None, errors: str = None) -> bytes: 
            """
            Encode the string using the codec registered for encoding.

            encoding
                The encoding in which to encode the string.
            errors
                The error handling scheme to use for encoding errors.
                The default is 'strict' meaning that encoding errors raise a
                UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
                'xmlCharrefReplace' as well as any other name registered with
                codecs.register_error that can handle UnicodeEncodeErrors.
            """
            return str.encode(self,encoding,errors)
        @staticmethod
        def endswith(self:str,suffix:str,start: int = None, end: int = None) -> bool:
            """
            S.endswith(suffix[, start[, end]]) -> bool

            Return True if S ends with the specified suffix, False otherwise.
            With optional start, test S beginning at that position.
            With optional end, stop comparing S at that position.
            suffix can also be a tuple of strings to try.
            """ 
            return str.endswith(self,suffix,start,end)
        @staticmethod
        def find(self:str,sub: str,start: int = None, end: int = None)->int:
            """
            S.find(sub[, start[, end]]) -> int

            Return the lowest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.

            Return -1 on failure.
            """ 
            return str.find(self,sub,start,end)
        @staticmethod
        def index(self:str,sub: str,start: int = None, end: int = None)->int:
            """
            S.index(sub[, start[, end]]) -> int

            Return the lowest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.

            Raises ValueError when the substring is not found.
            """ 
            return str.index(self,sub,start,end)
        @staticmethod
        def isalnum(self:str)->bool: 
            """
            Return True if the string is an alpha-numeric string, False otherwise.

            A string is alpha-numeric if all characters in the string are alpha-numeric and
            there is at least one character in the string.
            """
            return str.isalnum(self)
        @staticmethod
        def isalpha(self:str)->bool: 
            """
            Return True if the string is an alphabetic string, False otherwise.

            A string is alphabetic if all characters in the string are alphabetic and there
            is at least one character in the string.
            """
            return str.isalpha(self)
        @staticmethod
        def isdigit(self:str)->bool: 
            """
            Return True if the string is a digit string, False otherwise.

            A string is a digit string if all characters in the string are digits and there
            is at least one character in the string.
            """
            return str.isdigit(self)
        @staticmethod
        def islower(self:str)->bool: 
            """
            Return True if the string is a lowercase string, False otherwise.

            A string is lowercase if all cased characters in the string are lowercase and
            there is at least one cased character in the string.
            """
            return str.islower(self)
        @staticmethod
        def isspace(self:str)->bool: 
            """
            Return True if the string is a whitespace string, False otherwise.

            A string is whitespace if all characters in the string are whitespace and there
            is at least one character in the string.
            """
            return str.isspace(self)
        @staticmethod
        def istitle(self:str)->bool: 
            """
            Return True if the string is a title-cased string, False otherwise.

            In a title-cased string, upper- and title-case characters may only
            follow uncased characters and lowercase characters only cased ones.
            """
            return str.istitle(self)
        @staticmethod
        def isupper(self:str)->bool: 
            """
            Return True if the string is an uppercase string, False otherwise.

            A string is uppercase if all cased characters in the string are uppercase and
            there is at least one cased character in the string.
            """
            return str.isupper(self)
        @staticmethod
        def join(self:str,iterable: list[str])->bool: 
            """
            Concatenate any number of strings.

            The string whose method is called is inserted in between each given string.
            The result is returned as a new string.

            Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
            """
            return str.join(self,iterable)
        @staticmethod
        def ljust(self, width: int,fillChar: str = None) -> str: 
            """
            Return a left-justified string of length width.

            Padding is done using the specified fill character (default is a space).
            """
            return str.ljust(self,width,fillChar)
        @staticmethod
        def lower(self:str)->str: 
            """Return a copy of the string converted to lowercase."""
            return str.lower(self)
        @staticmethod
        def lstrip(self:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.

            If chars is given and not None, remove characters in chars instead.
            """
            return str.lstrip(self,chars)
        @staticmethod
        def partition(self:str,sep:str)->tuple[str,str,str]: 
            """
            Partition the string into three parts using the given separator.

            This will search for the separator in the string.  If the separator is found,
            returns a 3-tuple containing the part before the separator, the separator
            itself, and the part after it.

            If the separator is not found, returns a 3-tuple containing the original string
            and two empty strings.
            """
            return str.partition(self,sep)
        @staticmethod
        def replace(self:str,old:str,new:str,count:int=None)->str: 
            """
            Return a copy with all occurrences of substring old replaced by new.

            count
                Maximum number of occurrences to replace.
                -1 (the default value) means replace all occurrences.

            If the optional argument count is given, only the first count occurrences are
            replaced.
            """
            return str.replace(self,old,new,count)
        @staticmethod
        def rfind(self:str,sub: str,start: int = None, end: int = None)->int: 
            """
            S.rfind(sub[, start[, end]]) -> int

            Return the highest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.

            Return -1 on failure.
            """
            return str.rfind(self,sub,start,end)
        @staticmethod
        def rindex(self:str,sub: str,start: int = None, end: int = None)->int: 
            """
            S.rindex(sub[, start[, end]]) -> int

            Return the highest index in S where substring sub is found,
            such that sub is contained within S[start:end].  Optional
            arguments start and end are interpreted as in slice notation.

            Raises ValueError when the substring is not found.
            """
            return str.rindex(self,sub,start,end)
        @staticmethod
        def rjust(self, width: int,fillChar: str = None) -> str: 
            """
            Return a right-justified string of length width.

            Padding is done using the specified fill character (default is a space).
            """
            return str.rjust(self,width,fillChar)
        @staticmethod
        def rpartition(self:str,sep:str)->tuple[str,str,str]: 
            """
            Partition the string into three parts using the given separator.

            This will search for the separator in the string, starting at the end. If
            the separator is found, returns a 3-tuple containing the part before the
            separator, the separator itself, and the part after it.

            If the separator is not found, returns a 3-tuple containing two empty strings
            and the original string.
            """
            return str.rpartition(self,sep)
        @staticmethod
        def rsplit(self:str,sep:str,maxSplit:int=None)->list[str]: 
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
            return str.rsplit(self,sep,maxSplit)
        @staticmethod
        def rstrip(self:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.

            If chars is given and not None, remove characters in chars instead.
            """
            return str.rstrip(self,chars)
        @staticmethod
        def split(self:str,sep:str,maxSplit:int=None)->list[str]: 
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
            return str.split(self,sep,maxSplit)
        @staticmethod
        def splitlines(self:str,keepEnds:bool=None)->list[str]: 
            """
            Return a list of the lines in the string, breaking at line boundaries.

            Line breaks are not included in the resulting list unless keepEnds is given and
            true.
            """
            return str.splitlines(self,keepEnds)
        @staticmethod
        def startswith(self:str,suffix:str,start: int = None, end: int = None) -> bool: 
            """
            S.startswith(prefix[, start[, end]]) -> bool

            Return True if S starts with the specified prefix, False otherwise.
            With optional start, test S beginning at that position.
            With optional end, stop comparing S at that position.
            prefix can also be a tuple of strings to try.
            """
            return str.startswith(self,suffix,start,end)
        @staticmethod
        def strip(self:str,chars:str=None)->str: 
            """
            Return a copy of the string with leading whitespace removed.

            If chars is given and not None, remove characters in chars instead.
            """
            return str.strip(self,chars)
        @staticmethod
        def swapcase(self:str)->str: 
            """Convert uppercase characters to lowercase and lowercase characters to uppercase."""
            return str.swapcase(self)
        @staticmethod
        def title(self:str)->str: 
            """
            Return a version of the string where each word is titleCased.

            More specifically, words start with upperCased characters and all remaining
            cased characters have lower case.
            """
            return str.title(self)
        @staticmethod
        def upper(self:str)->str: 
            """Return a copy of the string converted to uppercase."""
            return str.upper(self)
        @staticmethod
        def zfill(self:str,width: int)->str: 
            """Pad a numeric string with zeros on the left, to fill a field of the given width."""
            return str.zfill(self,width)

    class Math():
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

        #  self.model.addFunction('timedelta',timedelta)
        #  self.model.addFunction('timezone',pytz.timezone) 

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

    class Array():

        @staticmethod
        def foreach(list:list[Operand],item:str,method:Operand): pass
        @staticmethod
        def map(list:list[Operand],item:str,method:Operand)->list[Operand]: pass
        @staticmethod
        def filter(list:list[Operand],item:str,method:Operand)->list[Operand]: pass
        @staticmethod
        def reverse(list:list[Operand],item:str,method:Operand)->list[Operand]: pass
        @staticmethod
        def first(list:list[Operand],item:str,method:Operand)->Operand: pass
        @staticmethod
        def last(list:list[Operand],item:str,method:Operand)->Operand: pass

        @staticmethod
        def sort(list:list[Operand],item:str,method:Operand)->list[Operand]: pass
        @staticmethod
        def push(list:list[Operand],item:Operand): pass
        @staticmethod
        def pop(list:list[Operand],item:Operand): pass
        @staticmethod
        def remove(list:list[Operand],item:Operand): pass

        class ArrayForeach(ArrowFunction):   
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

        class ArrayMap(ArrowFunction):
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

        class ArrayFirst(ArrowFunction):
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

        class ArrayLast(ArrowFunction):
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

        class ArrayFilter(ArrowFunction):
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

        class ArrayReverse(ArrowFunction):
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
                
        class ArraySort(ArrowFunction):
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
                
        class ArrayPush(ArrowFunction):
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

        class ArrayPop(ArrowFunction):
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

        class ArrayRemove(ArrowFunction):
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
                                    
    class Signal():
        @staticmethod
        def listen(key:str)->any: pass 
        @staticmethod
        def wait(datetime:datetime)->any: pass
        @staticmethod
        def listeners(keys:list[str],time:datetime=None)->str: pass 

        class Listen(FunctionRef):
            def solve(self,values,token:Token)->Value:
                if len(values) == 0:                                    
                    value = self._children[0].eval(token)
                    if token.isBreak: return value
                    values.append(value.value)
                    signal = Signal(values[0])
                    token.addListener(signal)
                    return Value()
                else:
                    if values[0] in token.signals:
                        token.clearListeners()
                    return Value()               

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

        class Listeners(FunctionRef):
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
                    
                    
                         
                
                                
                