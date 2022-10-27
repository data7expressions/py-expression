import re
import copy
import numpy as np
from typing import List
from py_expression.contract.base import *
from py_expression.contract.operands import *
from .factory import ConstBuilder

class ValidatorHelper():
    def __init__(self):        
        self._reInt = re.compile('[0-9]+$')
        self._reDecimal = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')
        
    def isAlpha(self,value:str)->bool:
        if value == None:
            return False
        return value.isalpha()      
    def isAlphanumeric(self,value:str)->bool:
        if value == None:
            return False
        return value.isalnum()    
    def between(value:any,start:any,to:any)->bool:
        return value >= start and value <= to
    def includes(self,source:any,value:any)->bool:
        if isinstance(source, str):
            return value in source
        elif np.ma.isarray(source):
            return value in np.array(source)
        return False
        
    def isNull(self,value:any)->bool:
        return value == None
    def isNotNull(self,value:any)->bool:
        return value != None
    def isEmpty(self,value:str)->bool:
        return  value==None or value ==""
    def isNotEmpty(self,value:str)->bool:
        return  value!=None and value !=""
    def isBoolean(self,value:any)->bool:
        # https://stackoverflow.com/questions/15019830/check-if-object-is-a-number-or-boolean
        return isinstance(value[0], (int, float))
    def isNumber(self,value:any)->bool:
        return isinstance(value, (int, float))
    def isPositiveInteger(self,value:any)->bool:
        return isinstance(value, int) and int(value) >= 0
    def isInteger(self,value:any)->bool:
        return isinstance(value, int)
    def isDecimal(self,value:any)->bool:
        return isinstance(value, float)
    def isString(self,value:any)->bool:
        return isinstance(value, str)
    def isDate(self,value:any)->bool:
        pass
    def isDateTime(self,value:any)->bool:
        pass
    def isTime(self,value:any)->bool:
        pass
    def isObject(self,value:any)->bool:
        return isinstance(value, dict)
    def isArray(self,value:any)->bool:
        return np.ma.isarray(value)
    def isBooleanFormat(self,value:str)->bool:
        return value == 'true' or value == 'false'
    def isNumberFormat(self,value:str)->bool:
        return self.isDecimal(value)
    def isIntegerFormat(self,value:str)->bool:
        return self._reInt.match(value)
    def isDecimalFormat(self,value:str)->bool:
        return self._reDecimal.match(value)
    def isDateFormat(self,value:str)->bool:
        pass
    def isDateTimeFormat(self,value:str)->bool:
        pass
    def isTimeFormat(self,value:str)->bool:
        pass
    
class OperandHelper():
    
    def clone (self, operand: Operand)->Operand:
        return copy.copy(operand)
	
    def toExpression (self, operand: Operand)->str:
        list: List[str] = []
        if operand.type in [OperandType.Const,OperandType.Var]:
            list.append(operand.name)
        elif operand.type == OperandType.List:
            list.append('[')
            i = 0
            for i, child in enumerate(operand.children):
                if (i > 0): list.append(',')
                list.append(self.toExpression(child))			
            list.append(']')
        elif operand.type == OperandType.KeyVal:
            list.append(operand.name + ':')
            list.append(self.toExpression(operand.children[0]))
        elif operand.type == OperandType.Obj:
            list.append('{')
            for i,child in enumerate(operand.children):
                if (i > 0):list.append(',')
                list.append(self.toExpression(child))			
            list.append('}')
        elif operand.type == OperandType.Operator:
            if len(operand.children) == 1:
                list.append(operand.name)
                list.append(self.toExpression(operand.children[0]))
            elif len(operand.children) == 2:
                list.append('(')
                list.append(self.toExpression(operand.children[0]))
                list.append(operand.name)
                list.append(self.toExpression(operand.children[1]))
                list.append(')')			
        elif operand.type == OperandType.CallFunc:
            list.append(operand.name)
            list.append('(')
            for i,child in enumerate(operand.children):
                if (i > 0): list.append(',')
                list.append(self.toExpression(child))			
            list.append(')')
        elif operand.type == OperandType.ChildFunc:
            list.append(self.toExpression(operand.children[0]))
            list.append('.' + operand.name)
            list.append('(')
            for i,child in enumerate(operand.children):
                if (i > 1): list.append(',')
                list.append(self.toExpression(operand.children[i]))			
            list.append(')')
        elif operand.type == OperandType.Arrow:
            list.append(self.toExpression(operand.children[0]))
            list.append('.' + operand.name)
            list.append('(')
            list.append(operand.children[1].name)
            list.append('=>')
            list.append(self.toExpression(operand.children[2]))
            list.append(')')
        else:
            raise Exception('node: ' + operand.type + ' not supported')
        return list.join('')
	
    def objectKey (self,obj:dict)->any:
        keys = obj.keys().sort()
        list:List[str] = []
        for key in keys:
            list.append(key)
            list.append(str(obj[key]))		
        return list.join('|')	

    def getKeys (self,variable:Operand, fields: List[Operand], list: List[any], context: Context)-> List[any]:
        keys:List[any] = []
		# loop through the list and group by the grouper fields
        for item in list:
            key = ''
            values = []
            for keyValue in fields:
                context.data.set(variable.name, item)
				# variable.set(item)
                value = keyValue.children[0].eval(context)
                if type(value) is dict:
                    raise Exception('Property value '+ keyValue.name + ' is an object, so it cannot be grouped')
                key = value if key == '' else key+ '-' + value
                values.append({ 'name': keyValue.name, 'value': value })			
			# find if the key already exists in the list of keys
            # keys.find((p:any) => p.key === key)
            keyItem = next((p for p in keys if p.key == key ), None) 
            if keyItem != None:
				# if the key exists add the item
                keyItem.items.append(item)
            else:
				# if the key does not exist add the key, the values and the item
                keys.push({ 'key': key, 'values': values, 'items': [item], 'summarizers': [] })		
        return keys	

    def haveAggregates (self, operand: Operand)-> bool:
        if (not (operand.type == OperandType.Arrow) and operand.type == OperandType.CallFunc and  operand.name in ['avg', 'count', 'first', 'last', 'max', 'min', 'sum']):
            return True
        elif (operand.children and len(operand.children) > 0):
            for child in operand.children:
                if (self.haveAggregates(child)):
                    return True
        return False

    def findAggregates (self, operand: Operand)-> List[Operand]:
        if (not (operand.type == OperandType.Arrow) and operand.type == OperandType.CallFunc and operand.name in ['avg', 'count', 'first', 'last', 'max', 'min', 'sum']):
            return [operand]
        elif operand.children and len(operand.children) > 0:
            aggregates:List[Operand] = []
            for child in operand.children:
                childAggregates = self.findAggregates(child)
                if len(childAggregates) > 0:
                    aggregates = aggregates.concat(childAggregates)
            return aggregates
        return []

    def solveAggregates (self, list: List[any], variable: Operand, operand: Operand, context: Context)-> Operand:
        if (not(operand.type == OperandType.Arrow) and operand.type == OperandType.CallFunc and operand.name in ['avg', 'count', 'first', 'last', 'max', 'min', 'sum']):
            value:None
            if operand.name == 'avg':
                value = self.avg(list, variable, operand.children[0], context)
            elif operand.name == 'count':
                value = self.count(list, variable, operand.children[0], context)
            elif operand.name == 'first':
                value = self.first(list, variable, operand.children[0], context)
            elif operand.name == 'last':
                value = self.last(list, variable, operand.children[0], context)
            elif operand.name == 'max':
                value = self.max(list, variable, operand.children[0], context)
            elif operand.name == 'min':
                value = self.min(list, variable, operand.children[0], context)
            elif operand.name == 'sum':
                value = self.sum(list, variable, operand.children[0], context)
            return ConstBuilder().build(operand.pos, value)
        elif (operand.children != None and len(operand.children) > 0):
            for i,child in  enumerate(operand.children):
                operand.children[i] = self.solveAggregates(list, variable, child, context)
        return operand	

    def count (self,list: List[any], variable: Operand, aggregate: Operand, context: Context)-> int:
        count = 0
        for item in list:
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                count+=1
        return count	

    def first (self,list: List[any], variable: Operand, aggregate: Operand, context: Context)->any:
        for item in list:
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                return item
        return None

    def last (self,list: List[any], variable: Operand, aggregate: Operand, context: Context)-> any:
        i = len(list)
        while i >= 0:
            item = list[i]
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                return item
            i-=1
        return None

    def max (self, list: List[any], variable: Operand, aggregate: Operand, context: Context)->any:
        max=None
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if (max == None or (value != None and value > max)):
                max = value
        return max

    def min (self, list: List[any], variable: Operand, aggregate: Operand, context: Context)-> any:
        min:None
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if min == None or (value != None and value < min):
                min = value
        return min	

    def avg (self,list: List[any], variable: Operand, aggregate: Operand, context: Context)-> float:
        sum = 0
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if value != None:
                sum = sum + value
        return sum / list.length if list > 0 else 0	

    def sum (self,list: List[any], variable: Operand, aggregate: Operand, context: Context)-> float:
        sum = 0
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if value != None:
                sum = sum + value
        return sum

class ObjectHelper():
    def __init__(self,validator:ValidatorHelper):
        self.validator = validator
        
    def clone(self, obj:dict)->dict:
        return obj.copy() if obj != None else None
    
    def extends(self, obj: any, base: any)->any:
        if np.ma.isarray(base):
            for baseChild in base:
                objChild =  self.__find(obj,baseChild.name)
                if objChild == None:
                    obj.append(baseChild.copy())
                else:
                    self.extends(objChild, baseChild)
        elif type(base) is dict:
            for entry in base.items():
                if entry[1] == None:
                   obj[entry[0]] = base[entry[0]].copy()  
                elif type(obj[entry[0]]) is dict:
                    self.extends(obj[entry[0]], base[entry[0]])
        return obj 
    
    def names(self, value:str)->any:
        if value == '.':
            # in case "".[0].name" where var is "."
            return [value]
        elif value.startswith('..'):
			#  in case ".name.filter"
            return (['.'] + value[2:]).split('.')
        elif value.startswith('.'):
			#  in case ".name.filter"
            return (['.'] + value[1:]).split('.')
        else:
            return value.split('.')		
                
    
    def getValue (self, source:any, name:str)->any:
        names = self.names(name)
        value = source
        for name in names:
            if np.ma.isarray(value):
				# Example: orders.0.number
                if self.validator.isPositiveInteger(name):
                    index = int(name)
                    value = value[index]
                    continue
                result = []
                for item in value:
                    if item[name] != None:
                        if np.ma.isarray(item[name]):
                            result = result + item[name]
                        else:
                            result.append(item[name])
                value = result
            else:
                if value[name] == None:
                    return None
                value = value[name]		
        return value
    
    def setValue (self, source:any, name:str, value:any):
        names = name.split('.')
        level = len(names) - 1
        data = source
        for i, name in enumerate(names):
			# if is an array and name is a positive integer
            if np.ma.isarray(data) and self.validator.isPositiveInteger(name):
                index = int(name)
				# If the index exceeds the length of the array, nothing assigns it.
                if index >= len(data):
                    return				
                if i == level:
                    data[index] = value
                else:
                    data = data[index]				
            else:
                if i == level:
                    data[name] = value
                else:
                    data = data[name]
    
    def sort(self, source: any)->any:
        target = {}
        for key in source.keys().sort():
            target[key] = source[key]		
        return target
    
    def fromEntries(self, entries:any)->any:
        if not np.ma.isarray(entries):
            return {}		
        obj:any = {}
        for element in entries :
            if not np.ma.isarray(element) or len(element) != 2:
                continue
            obj[element[0]] = element[1]		
        return obj
    
    def __find (self,array:any, name:str):
        for item in array:
            if item.name == name:
                return item
        return None        
        
class ExpHelper():
    def __init__(self):
        self._validator = ValidatorHelper()
        self._operand = OperandHelper()
        self._obj = ObjectHelper(self._validator)
        
    @property
    def validator(self):
        return self._validator
   
    @property
    def operand(self):
        return self._operand
    
    @property
    def obj(self):
        return self._obj   

helper = ExpHelper()