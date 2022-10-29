from lib.expression import Exp

try:
    # result = Exp.eval('a*3==b+1',{"a":1,"b":2})
    # result = Exp.eval('a.foreach(p=>b=b+p)',{"a":[1,2,3],"b":0})
    result = Exp.eval('1+2',{})
    print(result)    
           
except Exception as ex:
    print(ex) 
