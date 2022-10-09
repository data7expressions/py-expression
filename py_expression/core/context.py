
class Context():
    def __init__(self,data:dict={},parent:'Context'=None):
        self.data = data
        self._parent= parent

    def newContext(self):        
        return Context({},self)

    def getContext(self,variable):
        if variable in self.data or self._parent is None: return self.data
        _context =self._parent.getContext(variable)
        return _context  if _context is not None else self.data

    def get(self,name):
        names=name.split('.')
        value = self.getContext(names[0]) 
        for n in names:
            if n not in value: return None
            value=value[n]
        return value

    def set(self,name,value):
        names=name.split('.')        
        level = len(names)-1
        list = self.getContext(names[0]) 
        for i,e in enumerate(names):
            if i == level:
                list[e]=value
            else:                    
                list=list[e] 

    def init(self,name,value):
        self.data[name]=value   