from enum import Enum
from typing import TypeVar, Generic, List, Union
from lib.contract.base import Singleton
import numpy as np
import json

class Kind(Enum):
    any = 'any'
    string = 'string'
    integer = 'integer' 
    decimal = 'decimal'
    number = 'number'
    boolean = 'boolean'
    date = 'date'
    datetime = 'datetime'
    time = 'time'    
    void = 'void'
    obj = 'obj'
    list = 'list'
        
class PropertyType():
    def __init__(self, name:str, type:'Type'):
        self.name = name
        self.type = type
        
class ObjType():
    def __init__(self, properties: list[PropertyType]):
        self.properties = properties

class ListType():
    def __init__(self, items: 'Type'):
        self.items = items

class Type(metaclass=Singleton):
    def __init__(self, kind:Kind, spec:Union[ObjType, ListType, None]=None):
        self.kind = kind
        self.spec = spec  
        
    @staticmethod
    def any ()-> 'Type':
        return Type(Kind.any)
    
    @staticmethod
    def string ()-> 'Type':
        return Type(Kind.string)
    
    @staticmethod
    def integer ()-> 'Type':
        return Type(Kind.integer)
    
    @staticmethod
    def decimal ()-> 'Type':
        return Type(Kind.decimal)
    
    @staticmethod
    def any ()-> 'Type':
        return Type(Kind.any)
    
    @staticmethod
    def number ()-> 'Type':
        return Type(Kind.number)
    
    @staticmethod
    def boolean ()-> 'Type':
        return Type(Kind.boolean)
    
    @staticmethod
    def date ()-> 'Type':
        return Type(Kind.date)
    
    @staticmethod
    def datetime ()-> 'Type':
        return Type(Kind.datetime)
    
    @staticmethod
    def time ()-> 'Type':
        return Type(Kind.time)
    
    @staticmethod
    def void ()-> 'Type':
        return Type(Kind.void)
    
    @staticmethod
    def obj (properties: List[PropertyType] = [])-> 'Type':
        return Type(Kind.obj, { properties: properties })
    
    @staticmethod
    def list (items:'Type') -> 'Type':
        return Type(Kind.list, { items: items })
	
    @staticmethod
    def isPrimitive (type:Union['Type', str])-> boolean:
        if isinstance(type,str):
            value = type
        elif type != None and type.kind != None:
            value = str(type.kind)
        else:
            return False		
        return value in ['string', 'integer', 'decimal', 'number', 'boolean', 'date', 'datetime', 'time']	

    @staticmethod
    def to (kind:Union['Type', str])-> 'Type': 
        if isinstance(type,str):
            kindKey = str(kind)
            return Type(Kind[kindKey])
        return Type(kind)	

    @staticmethod
    def get (value: any)-> 'Type':
        if value == None:
            return Type.any()
        elif np.ma.isarray(value):
            if len(value) > 0:
                return Type.list(Type.get(value[0]))			
            return Type.any()
        elif isinstance(value,dict):
            properties:List[PropertyType] = []
            for key, value in value.items():
                properties.push({ 'name': key, 'type': Type.get(value) })			
            return Type.obj(properties)
        elif isinstance(value,str):
            # TODO determinar si es fecha.
            return Type.string()
        elif isinstance(value,int):			
            return Type.integer()
        elif isinstance(value,float):			
            return Type.decimal()
        elif isinstance(value,bool):
            return Type.boolean()
        return Type.any()

    @staticmethod
    def isList (type: Union['Type', str])-> bool:
        if isinstance(type,str):
            return type.startswith('[') and type.endswith(']')		
        return type.kind == Kind.list
	

    @staticmethod
    def isObj (type: Union['Type', str])-> bool:
        if isinstance(type, str):
            return type.startswith('{') and type.endswith('}')		
        return type.kind == Kind.obj
	

    @staticmethod
    def toString (type: 'Type'=None)-> str:
        if type == None:
            return 'any'		
        if Type.isPrimitive(type):
            return str(type.kind)		
        if Type.isObj(type):
            properties:List[str] = []			
            for propertyType in type.spec.properties:
                properties.append(propertyType.name+':'+Type.toString(propertyType.type))			
            return ','.join(properties)		
        if Type.isList(type):			
            return '['+Type.toString(type.spec.items)+']'		
        return 'any'
	

    @staticmethod
    def serialize (type: 'Type'= None)->str:
        if type == None:
            return None		
        return json.dumps(type)
	

    @staticmethod
    def deserialize (type: str=None)-> 'Type':
        if type == None or type.strip() == '':
            return None		
        return json.load(type)
	
	