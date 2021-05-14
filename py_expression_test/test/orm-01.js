

// class Orm {

//     exec(sentence,args){
//         const fnString = Function.prototype.toString.call(sentence);
//         console.log(fnString)
//         console.log(args)
//     }
// }
// orm = new Orm()

dataExec(cnx,sentence);
sentence1 = dataSentence(sentence);

sentence3 = sentence1 && sentence2
result = await(dataExec(cnx,sentence3));

sentence = (ORM)=> Product.select(p=> {category=p.category.name,total=sum(p.cost)})
                        .where(p=> p.category != a )                     
                        .having(p=> p.total > 100 )
                        .sort(p=> desc(p.category));

//example query with having
result = await(dataExec($DbCnx,sentence,{a:1}));

// Filter using subquery 
callback = dataExec($DbCnx,()=> Product.select(p=> {category=p.category.name,total=sum(p.cost)})
                                        .where( p=> p.category != a && !exists(Blacklist.where(q=> q.categoryId == p.categoryId))  )                     
                                        .having(p=> p.total > 100 )
                                        .sort(p=> desc(p.category) ) 
,{a:1});


//ejecuta en paralelo los callbacks y retornar un array con los resultados en el mismo orden que se paso.
results = parallel([callback])

// orm.exec( select(p=> ({category:p.category,total:sum(p.cost)}) )
//           .filter(p=> p.category != null && p.total > 100 )
//           .sort(p=> p.category)
//         );