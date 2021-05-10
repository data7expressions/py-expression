

function resursive(a){
    if (a>10){
        return a;
    }
    else{
       return resursive(a+1);
    };    
}
result = resursive(3) 