
from typing import TypeVar, Generic, List
import re
# https://stackoverflow.com/questions/6725868/generics-templates-in-python
T = TypeVar('T')

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ISerializer(Generic[T]):
    def serialize (self, value:T)-> dict:
        pass
    def deserialize (self, value: dict)-> T:
        pass
    def clone (self, value: T)-> T:
        pass

class ICache(Generic[T]): 
    def get(self, key:str)-> any:
        pass
    def set(self, key:str, value:any):
        pass
    def delete(self, key:str):
        pass
    
class Parameter():
    def __init__(self, name:str, type:str, value:any=None, default:any=None, multiple:bool=False ):
      self.name = name
      self.type = type
      self.value = value
      self.default = default
      self.multiple = multiple

class Sing():
    def __init__(self, name:str, params:List[Parameter], returnType:str, isAsync:bool=False ):
      self.name = name
      self.params = params
      self.returnType = returnType
      self.isAsync = isAsync
      
class Format():
    def __init__(self, name:str, pattern:str, regExp:re):
      self.name = name
      self.pattern = pattern
      self.regExp = regExp
  

class Position():
    def __init__(self, ln:int, col:int):
      self.ln = ln
      self.col = col

