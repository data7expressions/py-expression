from lib.expression import Exp

try:
    exp = Exp()
    # result = exp.eval('a*3==b+1',{"a":1,"b":2})
    # result = exp.eval('a.foreach(p=>b=b+p)',{"a":[1,2,3],"b":0})
    result = exp.eval('1+2',{})
    print(result)    
           
except Exception as ex:
    print(ex) 
