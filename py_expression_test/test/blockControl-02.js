list = [1,2,3,4,5,6];
b=1; 
for(a in list){
    b = a*b;
    if(b >10){
        break;
    };
}