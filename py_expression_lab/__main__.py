from py_expression.expression import Exp

exp = Exp()
try:
    # result = exp.run('a*3==b+1',{"a":1,"b":2})
    result = exp.run('a.foreach(p=>b=b+p)',{"a":[1,2,3],"b":0})
    print(result)
           
except Exception as ex:
    print(ex) 
