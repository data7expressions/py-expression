from lib.expression import exp

try:
    result = exp.eval('a*3==b+1',{"a":1,"b":2})
    # print(result) 
    # result = exp.eval('a.foreach(p=>b=b+p)',{"a":[1,2,3],"b":0})
    # result = exp.eval('(1+4)*2',{})
    # context = {"a":[1,2,3,4,5],"b":0}
    # result = exp.eval('a.first(p => p%2==0)',context)
    # context = {"a":[1,2,3,4,5],"b":0}
    # result = exp.eval('a.filter(p=> p>1 && p<5).map(p=> p*2)',context)
    # context = {"a":[1,2,3,4,5],"b":0}
    # result =exp.eval('a.filter(p=> p>1 && p<5).reverse()',context)
    print(result)    
           
except Exception as ex:
    print(ex) 
