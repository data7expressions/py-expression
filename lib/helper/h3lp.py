import re
import numpy as np

class ValidatorHelper():
    def __init__(self):        
        self._reInt = re.compile('[0-9]+$')
        self._reDecimal = re.compile('(\d+(\.\d*)?|\.\d+)([eE]\d+)?')
        self._reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$')
        self._reAlpha = re.compile('[a-zA-Z]+$')
        self._reDate = re.compile('^\d{4}-\d{2}-\d{2}$')
        self._reDateTime = re.compile('\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)')
        self._reTime = re.compile('\[0-2]\d:[0-5]\d:[0-5]\d')
        
    def isAlpha(self,value:str)->bool:
        if value == None:
            return False
        return self._reAlpha.match(value)      
    def isAlphanumeric(self,value:str)->bool:
        if value == None:
            return False
        return self._reAlphanumeric.match(value)  
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
        return self._reDate.match(value) 
    def isDateTimeFormat(self,value:str)->bool:
        return self._reDateTime.match(value) 
    def isTimeFormat(self,value:str)->bool:
        return self._reTime.match(value) 

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
        
class H3lp():
    def __init__(self):
        self._validator = ValidatorHelper()
        self._obj = ObjectHelper(self._validator)
        
    @property
    def validator(self):
        return self._validator
    
    @property
    def obj(self):
        return self._obj 

h3lp = H3lp()
