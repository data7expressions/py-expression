import time as t

class General():
    @staticmethod
    def nvl(a:any,b:any)->any: 
        return a if a!=None and a!="" else b 
    @staticmethod
    def isEmpty(a:any)->bool:return  a==None or a =="" 
    @staticmethod
    def sleep(secs:float): return t.sleep(secs)


class String():
     # https://docs.python.org/2.5/lib/string-methods.html
    @staticmethod
    def capitalize(self:str):
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

