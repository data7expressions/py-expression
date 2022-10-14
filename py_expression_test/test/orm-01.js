


sentence1 = Product.select(p=> {category=p.category.name,total=sum(p.cost)})
                .where(p=> p.category != a )                     
                .having(p=> p.total > 100 )
                .sort(p=> desc(p.category));

// Filter using subQuery 
sentence2 = Product.select(p=> {category=p.category.name,total=sum(p.cost)})
                .where( p=> p.category != a && !exists(Blacklist.where(q=> q.categoryId == p.categoryId))  )                     
                .having(p=> p.total > 100 )
                .sort(p=> desc(p.category))
                .params({a:1});             
// ejecuta la sentencia y retorna el resultado
result= sentence1.execute()
// ejecuta y asigna los parámetros, si alguno estaba definido, lo reemplaza
result= sentence1.params({b:1}).execute()   

//ejecuta en paralelo los callbacks y retornar un array con los resultados en el mismo orden que se paso.
results = parallel([sentence1,sentence2])

