try{
    if(a == null){
        throw 'is null'; 
    }else if (a == 0){
        throw 'a is 0'; 
    }; 
}catch(error){
    console.log(error);
    throw error;
};