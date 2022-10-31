import re
from typing import Any
from lib.helper.h3lp import h3lp
from lib.contract.base import *
from lib.contract.operands import *
from .factory import ConstBuilder
import copy

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
	
    def objectKey (self,obj:dict)->Any:
        keys = obj.keys().sort()
        list:List[str] = []
        for key in keys:
            list.append(key)
            list.append(str(obj[key]))		
        return list.join('|')	

    def getKeys (self,variable:Operand, fields: List[Operand], list: List[Any], context: Context)-> List[Any]:
        keys:List[Any] = []
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
            # keys.find((p:Any) => p.key === key)
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

    def solveAggregates (self, list: List[Any], variable: Operand, operand: Operand, context: Context)-> Operand:
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

    def count (self,list: List[Any], variable: Operand, aggregate: Operand, context: Context)-> int:
        count = 0
        for item in list:
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                count+=1
        return count	

    def first (self,list: List[Any], variable: Operand, aggregate: Operand, context: Context)->Any:
        for item in list:
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                return item
        return None

    def last (self,list: List[Any], variable: Operand, aggregate: Operand, context: Context)-> Any:
        i = len(list) - 1
        while i >= 0:
            item = list[i]
            context.data.set(variable.name, item)
            if aggregate.eval(context):
                return item
            i-=1
        return None

    def max (self, list: List[Any], variable: Operand, aggregate: Operand, context: Context)->Any:
        max=None
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if (max == None or (value != None and value > max)):
                max = value
        return max

    def min (self, list: List[Any], variable: Operand, aggregate: Operand, context: Context)-> Any:
        min:None
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if min == None or (value != None and value < min):
                min = value
        return min	

    def avg (self,list: List[Any], variable: Operand, aggregate: Operand, context: Context)-> float:
        sum = 0
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if value != None:
                sum = sum + value
        return sum / len(list) if list > 0 else 0	

    def sum (self,list: List[Any], variable: Operand, aggregate: Operand, context: Context)-> float:
        sum = 0
        for item in list:
            context.data.set(variable.name, item)
            value = aggregate.eval(context)
            if value != None:
                sum = sum + value
        return sum
      
class ExpHelper():
    def __init__(self):
        self._operand = OperandHelper()
   
    @property
    def operand(self):
        return self._operand
    
    @property
    def validator(self):
        return h3lp.validator
    
    @property
    def obj(self):
        return h3lp.obj 
  

helper = ExpHelper()