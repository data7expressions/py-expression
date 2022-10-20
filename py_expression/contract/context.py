from py_expression.helper.helper import helper
import uuid

class Data():
    def __init__(self,data:dict={},parent:'Data'=None):
        self.data = data
        self._parent= parent

    def newData(self)->'Data':        
        return Data({},self)

    def getData (self,variable):
        if variable in self.data or self._parent is None: return self.data
        _context =self._parent.getData(variable)
        return _context  if _context is not None else self.data

    def contains(self, name:str)->bool:
        names = name.split('.')
        value = self.getData(names[0])
        for name in names:
            if value[name] == None:
                return False
            value = value[name]		
        return True	

    def get(self,name):
        names= helper.obj.names(name)
        data = self.getData(names[0]) 
        return helper.obj.getValue(data, name)

    def set(self,name,value):
        names= helper.obj.names(name)
        data = self.getData(names[0])
        helper.obj.setValue(data, name, value) 

    def init(self,name,value):
        self.data[name]=value   

class Step():
    def __init__(self,name,id):
        self.name = name
        self.id = id
        self.values = []
    
class Token():
    def __init__(self):
        self.id= str(uuid.uuid4())
        self.stack = {}
        self.isBreak= False
        self.listeners = [] 
        self.signals = []     

    def addListener(self,value):
        self._isBreak = True 
        self._listeners.append(value)

    def clearListeners(self):
        self._isBreak = False 
        self._listeners = [] 

    def addSignal(self,value):
        self._signals.append(value)

    def clearSignals(self):
        self._signals = []                 

class Context():
    def __init__(self,data:Data, token:Token=None, parent:'Context'=None):
        self.data = data if data is not None else Data({})
        self.token = token if token is not None else Token()
        self._parent= parent

    def newContext(self):        
        return Context(self.data.newData(), self.token,self)