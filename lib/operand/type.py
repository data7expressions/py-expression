from lib.contract.base import *
from lib.contract.operands import *
from lib.contract.type import *
from lib.contract.managers import *


class TypeManager(ITypeManager):
    def __init__ (self, model: IModelManager):
        self.model = model

	# // Example
	# // {
	# // users:[{name:str,age:integer}],
	# // tuple: [integer,str]
	# // entries:[str,any]
	# // }
	# // Primitives: integer, decimal, str, boolean, datetime, date, time
	# // array: [<<type>>]
	# // object {key:<<type>>}
	# // predicate:  c + b < a
	# // indeterminate: any

    def parameters (self, operand: Operand)-> List[Parameter]:
        parameters: List[Parameter] = []
        if operand.type == OperandType.Var:
            parameters.append({ 'name': operand.name, 'type': Type.tostr(operand.returnType) })		
            for child in operand.children:
                childParameters = self.parameters(child)
                newParameters = next(p for p in childParameters if  not p.name in map(lambda q: q.name, parameters))
                # newParameters =   childParameters.filter((p:Parameter) => !parameters.map((p:Parameter) => p.name).includes(p.name))
                if len(newParameters) > 0:
                    parameters.extend(newParameters)    
        return parameters

    def type (self,operand: Operand)->Type:
        self.solveType(operand)
        self.solveTemplate(operand)
        self.setNoneAsAny(operand)
        return operand.returnType or Type.any
	

    def solveType (self,operand: Operand): 
        if operand.type == OperandType.Const or operand.type == OperandType.Var or operand.type == OperandType.Template:
            return		
        if operand.type == OperandType.List:
            self.solveArray(operand)
        elif operand.type == OperandType.Obj:
            self.solveObject(operand)
        elif operand.type == OperandType.Arrow:
            self.solveArrow(operand)
        elif operand.type == OperandType.Operator or operand.type == OperandType.ChildFunc or operand.type == OperandType.CallFunc:
            self.solveOperator(operand)
        elif operand.type == OperandType.Property:
            self.solveProperty(operand)
        else:
            raise Exception(operand.type +' '+ operand.name + ' not supported')	

    def solveTemplate (self, operand: Operand):
        if operand.type == OperandType.Const or operand.type == OperandType.Var or operand.type == OperandType.Template:
            return
        if operand.type == OperandType.List:
            self.solveTemplateArray(operand)
        elif (operand.type == OperandType.Obj):
            self.solveTemplateObject(operand)
        elif (operand.type == OperandType.Operator or operand.type == OperandType.Arrow or operand.type == OperandType.ChildFunc or operand.type == OperandType.CallFunc):
            metadata = self.metadata(operand)
            if self.hadTemplate(metadata) and self.NoneTypes(operand):
                self.solveTemplateOperator(operand, metadata)			
            for child in operand.children:
                self.solveTemplate(child)
        elif (operand.type == OperandType.Property):
            self.solveTemplateProperty(operand)
        else:
            raise Exception(operand.type + ' ' + operand.name + ' not supported')

    def setNoneAsAny (self, operand: Operand):
        if (operand.returnType == None):
            operand.returnType = Type.any
        for child in operand.children:
            self.setNoneAsAny(child)

    def solveObject (self, obj: Operand):
        properties: List[PropertyType] = []
        for child in obj.children:
            self.solveType(child.children[0])
            properties.push({ 'name': child.name, 'type': child.children[0].returnType })
        obj.returnType = Type.obj(properties)

    def solveProperty (self, property: Operand):
        self.solveType(property.children[0])
        if (property.children[0].returnType == None):
            property.children[0].returnType = Type.list(Type.obj([{ 'name': property.name }]))
        elif (Type.isList(property.children[0].returnType)):
            listType = property.children[0].returnType.spec
            if (listType.items and Type.isObj(listType.items)):
                objectType = listType.items.spec
                propertyType = next(p for p in objectType.properties if p.name == property.name)
                if (propertyType and propertyType.type):
                    property.returnType = propertyType.type

    def solveArray (self, array: Operand):
        self.solveType(array.children[0])
		# si se resolvió el tipo del elemento, el tipo del array sera [<<TYPE>>]
        if (array.children[0].returnType !=None):
            array.returnType = Type.list(array.children[0].returnType)

    def solveArrow (self, arrow: Operand):
        metadata = self.model.getFunction(arrow.name)
        array = arrow.children[0]
        variable = arrow.children[1] if arrow.children.length > 1 else None
        predicate =  arrow.children[2] if arrow.children.length > 2 else None
        self.solveArray(array)
        elementType = self.getElementType(array)
        if (elementType and array.returnType and variable):
            variable.returnType = elementType
            if (predicate):
                self.setVariableType(variable.name, elementType, predicate)
        if not self.isIndeterminateType(metadata.returnType):
			# TODO: hay que hacer que se pueda convertir de metadata type a Type y viceversa
            arrow.returnType = Type.to(metadata.returnType)
        if (array.returnType == None and metadata.params[0].type and not self.isIndeterminateType(metadata.params[0].type)):
			# TODO: hay que hacer que se pueda convertir de metadata type a Type y viceversa
            array.returnType = Type.to(metadata.params[0].type)
        if (predicate and metadata.params[1].type and not self.isIndeterminateType(metadata.params[1].type)):
			# TODO: hay que hacer que se pueda convertir de metadata type a Type y viceversa
            predicate.returnType = Type.to(metadata.params[1].type)
        if (predicate):
            self.solveType(predicate)
        if (self.hadTemplate(metadata)):
            self.solveTemplateOperator(arrow, metadata)

    def solveOperator (self, operator: Operand):
        metadata = self.metadata(operator)
		# intenta resolver el return type por metadata
        if (not self.isIndeterminateType(metadata.returnType)):
            returnType = self.trySolveFromMetadata(metadata.returnType)
            if (returnType):
                operator.returnType = returnType
		# tries to resolve the types of the operands
        i = 0
        while i < len(metadata.params):
            paramInfo = metadata.params[i]
            operand = operator.children[i]
            if (operand == None):
                break
            if (self.isIndeterminateType(paramInfo.type)):
                continue
            # intenta resolver el tipo del operand por metadata
            paramType = self.trySolveFromMetadata(paramInfo.type)
            if (paramType):
                operand.returnType = paramType
            i+=1
        for child in operator.children:
            self.solveType(child)
        if self.hadTemplate(metadata):
            self.solveTemplateOperator(operator, metadata)

    def trySolveFromMetadata (self, type:str=None)->Type | None:
		# si de acuerdo a la metadata el tipo es primitivo, asigna el tipo
        if (type == None):
            return None		
        if (Type.isPrimitive(type)):
            return Type.to(type)
		# si de acuerdo a la metadata el tipo es un array de primitivo, asigna el tipo, example: str[]
        if type.endswith('[]'):
            elementType = type.substr(0, type.length - 2)
            if Type.isPrimitive(elementType):
                return Type.list(Type.get(elementType))
        return None

    def solveTemplateArray (self, array: Operand):
        beforeType = array.children[0].returnType
        self.solveTemplate(array.children[0])
        if (array.children[0].returnType and array.children[0].returnType !=beforeType):
            array.returnType = Type.list(array.children[0].returnType)

    def solveTemplateProperty (self, property: Operand):
        beforeType = property.children[0].returnType
        self.solveTemplate(property.children[0])
        if (property.children[0].returnType !=None and property.children[0].returnType !=beforeType and Type.isList(property.children[0].returnType)):
            arrayType = property.children[0].returnType.spec
            if (Type.isObj(arrayType.items)):
                objectType = arrayType.items.spec
                propertyType = next(p for p in objectType.properties if p.name == property.name)
                if (propertyType and propertyType.type):
                    property.returnType = propertyType.type

    def solveTemplateObject (self,obj: Operand):
        changed = False
        for child in obj.children:
            value = child.children[0]
            beforeType = value.returnType
            self.solveTemplate(value)
            if (value.returnType !=beforeType):
                changed = True
        if (changed):
            properties: List[PropertyType] = []
            for child in obj.children:
                properties.push({ 'name': child.name, 'type': child.children[0].returnType })
            obj.returnType = Type.obj(properties)

    def solveTemplateOperator (self, operator: Operand, metadata:OperatorMetadata):
        templateType:Type|None
		# intenta resolver T por return
        if (operator.returnType):
            if metadata.returnType == 'T':
                templateType = operator.returnType
            elif metadata.returnType == 'T[]' and Type.isList(operator.returnType):
                templateType = operator.returnType.spec.items
		# intenta resolver T por alguno de los parámetros
        if (templateType == None):
            i = 0
            while i < len(metadata.params):
                paramMetadata = metadata.params[i]
                if (paramMetadata.type !='T' and paramMetadata.type !='T[]'):
                    continue
                child = operator.children[i]
                if (child == None):
                    break
                if (child.returnType):
                    if (paramMetadata.type == 'T'):
                        templateType = child.returnType
                        break
                    elif (paramMetadata.type == 'T[]' and Type.isList(child.returnType)):
                        templateType = child.returnType.spec.items
                        break
                i+=1
		# si pudo resolver el T, resuelve donde se utiliza
        if (templateType !=None):
            if (operator.returnType == None):
                if (metadata.returnType == 'T'):
                    operator.returnType = templateType
                elif (metadata.returnType == 'T[]'):
                    operator.returnType = Type.list(templateType)
            i = 0
            while i < len(metadata.params):
                paramMetadata = metadata.params[i]
                if (paramMetadata.type !='T' and paramMetadata.type !='T[]'):
                    continue
                child = operator.children[i]
                if (child == None):
                    break
                if (child.returnType == None):
                    if (paramMetadata.type == 'T'):
                        child.returnType = templateType
                    elif (paramMetadata.type == 'T[]'):
                        child.returnType = Type.list(templateType)
                i+=1
    
    def getElementType (self, array: Operand)->Type | None:
        return array.returnType.spec.items if array.returnType else None

    def setVariableType (self,name: str, type: Type, operand: Operand):
        if (operand.type == OperandType.Var and operand.name == name):
            operand.returnType = type
        for child in operand.children:
			# es por si se da el caso  xxx.filter( p=> p.filter( p => p + 1 ) )
            if (not (child.type == OperandType.Arrow and child.children[1].name == name)):
                self.setVariableType(name, type, child)

    def isIndeterminateType (self, type:str=None)->bool:
        if (type == None):
            return True
        return type in ['T', 'T[]', 'any', 'any[]']

    def hadTemplate (self, metadata: OperatorMetadata)->bool:
        return metadata.returnType == 'T' or metadata.returnType == 'T[]' or  next(p for p in metadata.params if p.type == 'T' or p.type == 'T[]') !=None
	
    def NoneTypes (self, operator: Operand)->bool:
        return operator.returnType == None or next(p for p in operator.children if p.returnType == None) !=None
	
    def metadata (self, operator: Operand)-> OperatorMetadata:
        return self.model.getOperator(operator.name, len(operator.children)) if operator.type == OperandType.Operator else self.model.getFunction(operator.name)
