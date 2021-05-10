
class Process{
   
    start(){

    }
}
class Process01 extends Process
{
    constructor(a,b){
        this.a = a;
        this.b =b;
    }
    start(){
        if(this.a>this.b){    
            result=this.substraction(this.a,this.b)
        }else{
            result=this.substraction(this.b,this.a)
        }
        return result;
    }    
    substraction(a,b){
        return a-b
    }
}

result=Process01(2,4).start()