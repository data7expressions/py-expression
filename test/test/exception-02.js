
class Error01 extends Error{}
class Error02 extends Error{} 
class Error03 extends Error{} 

try{
    if(a == null){
        throw Error01('a is null'); 
    }else if (a == 0){
        throw Error01('a is 0'); 
    } 
}catch(error){
    if(is(error,Error01)){
        throw Error03('error 01')
    }else if (is(error,Error02)){
        throw Error03('error 02')
    } 
    throw error
};