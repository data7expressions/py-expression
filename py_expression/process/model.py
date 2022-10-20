from datetime import date,datetime,time,timedelta 
class Signal():
    def __init__(self,name:str,datetime:datetime=None):
        self.name= name
        self.datetime= datetime   

class WaitSignal(Signal):
    def __init__(self,name:str,secs:float=None):
        super(Signal,self).__init__(name) 
        self.secs = secs 