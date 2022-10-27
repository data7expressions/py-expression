from py_expression.contract.base import *
from py_expression.contract.operands import *
from py_expression.contract.type import *
from py_expression.operand.helper import helper
import os
import re 

class ConstEvaluator(Evaluator):
    def eval (self)-> any:
        if self.operand.returnType == None:
            return self.operand.name
        kind = self.operand.returnType.kind
        if kind == Kind.string:
            return self.operand.name
        elif kind == Kind.boolean:
            return bool(self.operand.name)
        elif kind == Kind.integer or kind == Kind.decimal or kind == Kind.number:
            return float(self.operand.name)
        else:
            return self.operand.name

class VarEvaluator(Evaluator):
    def eval (self,context: Context)-> any:
        return context.data.set(self.operand.name)    

class EnvEvaluator(Evaluator):
    def eval (self)-> any:
        return os.environ(self.operand.name) 

class TemplateEvaluator(Evaluator):
    def eval (self,context: Context)-> any:
        pass
    # def eval (self,context: Context)-> any:
    #     result = re.sub('\${([a-zA-Z0-9_.]+)}/g', lambda match, field : (
    #         value = os.environ[field]
    #         if value == None and context.data:
    #             value = context.data.get(field)			
    #         return match if value == None else value 
    #     )           
    #     ,self.operand.name)
    #     return result

class PropertyEvaluator(Evaluator):
    def eval (self,context: Context)-> any:
        value = self.operand.children[0].eval(context)
        if value == None:
            return None
        return helper.obj.getValue(value, self.operand.name)    

class ListEvaluator(Evaluator):
    def eval (self,context: Context)-> any:
        values=[]
        for i, p in enumerate(self.operand.children): 
            values.append(self.operand.children[i].eval(context))
        return values 

class ObjEvaluator(Evaluator):
    def eval (self,context: Context)-> any:
        obj= {}
        for i, child in enumerate(self.operand.children):
            obj[child.name] = child.children[0].eval(context) 
        return obj 
                              
class CallFuncEvaluator(Evaluator):
    def __init__(self,operand: Operand,function):
        super(CallFuncEvaluator,self).__init__(operand) 
        self._function = function

    def eval (self,context: Context)-> any:
        args = []
        for i, child in enumerate(self.operand.children): 
            args.append(child.eval(context))
        return self._function(*args)  
                
class IfEvaluator(Evaluator):
    def eval (self,context: Context)->any:
        condition = self.operand.children[0].eval(context)
        if condition:
            ifBlock = self.operand.children[1]
            return ifBlock.eval(context)
        elif len(self.operand.children) > 2:
            i=2
            while len(self.operand.children) > i:
                if self.operand.children[i].type == OperandType.ElseIf:
                    elseIfCondition = self.operand.children[i].children[0].eval(context)
                    if elseIfCondition != None:
                        elseIfBlock = self.operand.children[i].children[1]
                        return elseIfBlock.eval(context)
                else:
                    elseBlock = self.operand.children[i]
                    return elseBlock.eval(context)
         
class WhileEvaluator(Evaluator):
    def eval (self,context: Context)->any:
        lastValue= None
        condition = self.operand.children[0]
        block = self.operand.children[1]
        while condition.eval(context):
            lastValue = block.eval(context)
        return lastValue

class ForEvaluator(Evaluator):    
    def eval (self,context: Context)->any:
        lastValue= None
        initialize = self.operand.children[0]
        condition = self.operand.children[1]
        increment = self.operand.children[2]
        block = self.operand.children[3]
        initialize.eval(context)
        while condition.eval(context):
            lastValue = block.eval(context)
            increment.eval(context)
        return lastValue 

class ForInEvaluator(Evaluator):       
    def eval (self,context: Context)->any:
        lastValue= None
        item = self.operand.children[0]
        list = self.operand.children[1].eval(context)
        block = self.operand.children[2]
        i=0
        while len(list) > i:
            if context != None:
                context.data.set(item.name, list[i])
            lastValue = block.eval(context)
            i+=1    
        return lastValue   

class SwitchEvaluator(Evaluator):
    def eval (self,context: Context)->any:
        value = self.operand.children[0].eval(context)
        i=1
        while len(self.operand.children) > i:
            option = self.operand.children[i]
            if option.type == OperandType.Case:
                if option.name == value:
                    return option.children[0].eval(context)
            elif option.type == OperandType.Default:
                return option.children[0].eval(context)
            i+=1

class BreakEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')
  
class ContinueEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')

class FuncEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')

class ReturnEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')

class TryEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')

class CatchEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')

class ThrowEvaluator(Evaluator):
	def eval (self,context: Context)->any:
		raise Exception('NotImplemented')    