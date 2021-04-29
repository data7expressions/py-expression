import time as t
import math
from datetime import date,datetime,time,timedelta
from os import path,getcwd
from .base import *


class Operators():
    @staticmethod
    def addition(a,b):
        return a+b 
    @staticmethod
    def subtraction(a,b):
        return a-b   
    @staticmethod
    def multiplication(a,b):
        return a*b 
    @staticmethod
    def division(a,b):
        return a/b  
    @staticmethod
    def exponentiation(a,b):
        return a**b 
    @staticmethod
    def floorDivision(a,b):
        return a//b   
    @staticmethod
    def mod(a,b):
        return a%b 
    @staticmethod
    def bitAnd(a,b):
        return a & b 
    @staticmethod
    def bitOr(a,b):
        return a | b
    @staticmethod
    def bitXor(a,b):
        return a ^ b                  
    @staticmethod
    def bitNot(a):
        return ~ a
    @staticmethod
    def leftShift(a,b):
        return a << b   
    @staticmethod
    def rightShift(a,b):
        return a >> b   

    @staticmethod
    def equal(a,b):
        return a==b
    @staticmethod
    def notEqual(a,b):
        return a!=b          
    @staticmethod
    def greaterThan(a,b):
        return a>b
    @staticmethod
    def lessThan(a,b):
        return a<b 
    @staticmethod
    def greaterThanOrEqual(a,b):
        return a>=b
    @staticmethod
    def lessThanOrEqual(a,b):
        return a<=b               

    @staticmethod
    def _not(a):
        return not a

    @staticmethod
    def item(list,index):
        return list[index]

   



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
            'xmlcharrefreplace' as well as any other name registered with
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
    def ljust(self, width: int,fillchar: str = None) -> str: 
        """
        Return a left-justified string of length width.

        Padding is done using the specified fill character (default is a space).
        """
        return str.ljust(self,width,fillchar)
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
    def rjust(self, width: int,fillchar: str = None) -> str: 
        """
        Return a right-justified string of length width.

        Padding is done using the specified fill character (default is a space).
        """
        return str.rjust(self,width,fillchar)
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
    def rsplit(self:str,sep:str,maxsplit:int=None)->list[str]: 
        """
        Return a list of the words in the string, using sep as the delimiter string.

        sep
            The delimiter according which to split the string.
            None (the default value) means split according to any whitespace,
            and discard empty strings from the result.
        maxsplit
            Maximum number of splits to do.
            -1 (the default value) means no limit.

        Splits are done starting at the end of the string and working to the front.
        """
        return str.rsplit(self,sep,maxsplit)
    @staticmethod
    def rstrip(self:str,chars:str=None)->str: 
        """
        Return a copy of the string with leading whitespace removed.

        If chars is given and not None, remove characters in chars instead.
        """
        return str.rstrip(self,chars)
    @staticmethod
    def split(self:str,sep:str,maxsplit:int=None)->list[str]: 
        """
        Return a list of the words in the string, using sep as the delimiter string.

        sep
            The delimiter according which to split the string.
            None (the default value) means split according to any whitespace,
            and discard empty strings from the result.
        maxsplit
            Maximum number of splits to do.
            -1 (the default value) means no limit.
        """
        return str.split(self,sep,maxsplit)
    @staticmethod
    def splitlines(self:str,keepends:bool=None)->list[str]: 
        """
        Return a list of the lines in the string, breaking at line boundaries.

        Line breaks are not included in the resulting list unless keepends is given and
        true.
        """
        return str.splitlines(self,keepends)
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
        Return a version of the string where each word is titlecased.

        More specifically, words start with uppercased characters and all remaining
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

    #  self.addFunction('timedelta',timedelta)
    #  self.addFunction('timezone',pytz.timezone) 

class Volume():
            def __init__(self,_path):        
                self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
            def fullpath(self,_path):
                return path.join(self._root,_path)

class IO():
    # https://docs.python.org/3/library/os.path.html
    @staticmethod
    def Volume(_path:str)->Volume:
        """cretae Volume"""
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



class CoreLib(Library):
    def __init__(self):
       super(CoreLib,self).__init__()   
       self.initEnums()
       self.initOperators()
       self.generalFunctions()
       self.stringFunctions()
       self.mathFunctions()
       self.datetimeFunctions()
       self.ioFunctions()

    def initEnums(self): 
        self.addEnum('DayOfWeek',{"Monday":1,"Tuesday":2,"Wednesday":3,"Thursday":4,"Friday":5,"Saturday":6,"Sunday":0}) 

    def initOperators(self):       

        self.addOperator('+','arithmetic',Operators.addition,4)
        self.addOperator('-','arithmetic',Operators.subtraction,4)
        self.addOperator('*','arithmetic',Operators.multiplication,5)
        self.addOperator('/','arithmetic',Operators.division,5)
        self.addOperator('**','arithmetic',Operators.exponentiation,6)
        self.addOperator('//','arithmetic',Operators.floorDivision,6)
        self.addOperator('%','arithmetic',Operators.mod,7)

        self.addOperator('&','bitwise',Operators.bitAnd,4)
        self.addOperator('|','bitwise',Operators.bitOr,4)
        self.addOperator('^','bitwise',Operators.bitXor,4)
        self.addOperator('~','bitwise',Operators.bitNot,4)
        self.addOperator('<<','bitwise',Operators.leftShift,4)
        self.addOperator('>>','bitwise',Operators.rightShift,4)

        self.addOperator('==','comparison',Operators.equal,3)
        self.addOperator('!=','comparison',Operators.notEqual,3)
        self.addOperator('>','comparison',Operators.greaterThan,3)
        self.addOperator('<','comparison',Operators.lessThan,3)
        self.addOperator('>=','comparison',Operators.greaterThanOrEqual,3)
        self.addOperator('<=','comparison',Operators.lessThanOrEqual,3)

        # self.addOperator('&&','logical',And,2)
        # self.addOperator('||','logical',Or,2)
        self.addOperator('!','logical',Operators._not)

        self.addOperator('[]','list',Operators.item)
        

        # self.addOperator('=','assignment',Assigment,1)
        # self.addOperator('+=','assignment',AssigmentAddition,1)
        # self.addOperator('-=','assignment',AssigmentSubtraction,1)
        # self.addOperator('*=','assignment',AssigmentMultiplication,1)
        # self.addOperator('/=','assignment',AssigmentDivision,1)
        # self.addOperator('**=','assignment',AssigmentExponentiation,1)
        # self.addOperator('//=','assignment',AssigmentFloorDivision,1)
        # self.addOperator('%=','assignment',AssigmentMod,1)
        # self.addOperator('&=','assignment',AssigmentBitAnd,1)
        # self.addOperator('|=','assignment',AssigmentBitOr,1)
        # self.addOperator('^=','assignment',AssigmentBitXor,1)
        # self.addOperator('<<=','assignment',AssigmentLeftShift,1)
        # self.addOperator('>>=','assignment',AssigmentRightShift,1)        

    def generalFunctions(self):
        self.addFunction('nvl',General.nvl )
        self.addFunction('isEmpty',General.isEmpty)
        self.addFunction('sleep',General.sleep)        

    def stringFunctions(self):
        self.addFunction('capitalize',String.capitalize,'str')
        self.addFunction('count',String.count,'str')
        self.addFunction('encode',String.encode,'str')
        self.addFunction('endswith',String.endswith,'str')
        self.addFunction('find',String.find,'str')
        self.addFunction('index',String.index,'str')
        self.addFunction('isalnum',String.isalnum,'str')
        self.addFunction('isalpha',String.isalpha,'str')
        self.addFunction('isdigit',String.isdigit,'str')
        self.addFunction('islower',String.islower,'str')
        self.addFunction('isspace',String.isspace,'str')
        self.addFunction('istitle',String.istitle,'str')
        self.addFunction('isupper',String.isupper,'str')
        self.addFunction('join',String.join,'str')
        self.addFunction('ljust',String.ljust,'str')
        self.addFunction('lower',String.lower,'str')
        self.addFunction('lstrip',String.lstrip,'str')
        self.addFunction('partition',String.partition,'str')
        self.addFunction('replace',String.replace,'str')
        self.addFunction('rfind',String.rfind,'str')
        self.addFunction('rindex',String.rindex,'str')
        self.addFunction('rjust',String.rjust,'str')
        self.addFunction('rpartition',String.rpartition,'str')
        self.addFunction('rsplit',String.rsplit,'str')
        self.addFunction('rstrip',String.lstrip,'str')
        self.addFunction('split',String.split,'str')
        self.addFunction('splitlines',String.splitlines,'str')
        self.addFunction('startswith',String.startswith,'str')
        self.addFunction('strip',String.lstrip,'str')
        self.addFunction('swapcase',String.swapcase,'str')
        self.addFunction('title',String.title,'str')
        # self.addFunction('translate',String.translate,'str')
        self.addFunction('upper',String.upper,'str')
        self.addFunction('zfill',String.zfill,'str')   

    def mathFunctions(self):
        self.addFunction('ceil',Math.ceil)
        self.addFunction('copysign',Math.copysign) 
        self.addFunction('factorial',Math.factorial) 
        self.addFunction('floor',Math.floor) 
        self.addFunction('fmod',Math.fmod) 
        self.addFunction('frexp',Math.frexp) 
        self.addFunction('fsum',Math.fsum) 
        self.addFunction('isfinite',Math.isfinite) 
        self.addFunction('isnan',Math.isnan) 
        self.addFunction('ldexp',Math.ldexp) 
        self.addFunction('modf',Math.modf) 
        self.addFunction('trunc',Math.trunc) 
        self.addFunction('exp',Math.exp) 
        self.addFunction('expm1',Math.expm1) 
        self.addFunction('log',Math.log) 
        self.addFunction('log1p',Math.log1p) 
        self.addFunction('log2',Math.log2) 
        self.addFunction('log10',Math.log10) 
        self.addFunction('pow',Math.pow) 
        self.addFunction('sqrt',Math.sqrt) 
        self.addFunction('acos',Math.acos) 
        self.addFunction('asin',Math.asin) 
        self.addFunction('atan',Math.atan) 
        self.addFunction('atan2',Math.atan2) 
        self.addFunction('cos',Math.cos) 
        self.addFunction('hypot',Math.hypot) 
        self.addFunction('sin',Math.sin) 
        self.addFunction('tan',Math.tan) 
        self.addFunction('degrees',Math.degrees)
        self.addFunction('radians',Math.radians)
        self.addFunction('acosh',Math.acosh)
        self.addFunction('asinh',Math.asinh)
        self.addFunction('atanh',Math.atanh)
        self.addFunction('cosh',Math.cosh)
        self.addFunction('sinh',Math.sinh)
        self.addFunction('tanh',Math.tanh)
        self.addFunction('erf',Math.erf)
        self.addFunction('erfc',Math.erfc)
        self.addFunction('gamma',Math.gamma)
        self.addFunction('lgamma',Math.lgamma)
        self.addFunction('pi',Math.pi)
        self.addFunction('e',Math.e)
    
    def datetimeFunctions(self):
        self.addFunction('strftime',Date.strftime,'datetime')
        self.addFunction('strptime',Date.strptime)        
        self.addFunction('datetime',Date.datetime)
        self.addFunction('today',Date.today)
        self.addFunction('now',Date.now)
        self.addFunction('date',Date.date)
        self.addFunction('fromtimestamp',Date.fromtimestamp)
        self.addFunction('time',Date.time)
    
    def ioFunctions(self): 
        self.addFunction('Volume',IO.Volume)
        self.addFunction('pathRoot',IO.pathRoot)
        self.addFunction('pathJoin',IO.pathJoin)


