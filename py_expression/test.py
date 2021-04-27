
from typing import TypeVar, Generic

context = {"a":1,"b":2}

T = TypeVar('T')

class Operand():
    @property
    def value(self):
        return self._value 
    @value.setter
    def value(self,value):
        self._value =value       


def assigment(a:Operand,b:Operand)->Operand:
    a.value = b.value
    return a
    

assigment(context["a"],4)
print(context)