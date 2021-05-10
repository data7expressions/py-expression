//TODO: resolver metodos asincronicos

result=await(rest(url,action,body,headers,cookies)); 

result=await(rest(url(urlJoin($HOST,'/user/'+id),args),'GET',null,['context-type=json']));

promise=soap(url,action,body,headers,cookies); 
promise2=soap(url,action,body,headers,cookies); 

results = parallel(promise,promise2)