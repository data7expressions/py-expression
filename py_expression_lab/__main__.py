from py_expression.core import Exp,Token
from enum import Enum
from os import path

exp = Exp()
try:
    result = exp.run('a*3==b+1',{"a":1,"b":2})
    print(result)
           
except Exception as ex:
    print(ex) 
