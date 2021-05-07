class bpm2 {

    constructor(a,b){
        this.a =1
        this.b =2
        this.start()
    }    
    start(){
        this.evaluate()
    }
    evaluate(){
        //exclusiveGateway
        if(this.a>this.b)this.sum()
        else if(this.a<=this.b)this.subtraction()
    }
    sum(){
        this.a = this.a + this.b
    }
    subtraction(){
        this.a = this.a - this.b
    }
    end(){
        
    }
}

let a = new bpm2()