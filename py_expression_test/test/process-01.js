//TODO: Tener en cuenta que en los procesos se deberia pasar por los diferente steps/nodos sin guarda en la pila.
// solo se deberia guardar cual es el paso actual y el stack dentro de este paso.
// dado que si deneria salir y continuar , deberia ir directamente al paso/nodo actual

//al invocar un proceso, se debe generar un child token el cual quedara referenciado al token padre.

// Tener en cuenta:
// cuando se ejecuta un proceso este puede retornar en los siguientes casos
// por que finalizo: se debera mapear las variables de salida con las variables del proceso que lo invoco.
// por un break:
//          por signal: quedara en proceso en await y si el  proceso padre solo esta a la espera de espe subproceso tambien deberia quedar en await.
//          por errror: deberia quedar en error , si el proceso padre tiene un catch de error, lo podria capturar , caso contrario tambien quedaria en error.    


class Process{
    
    constructor(starts){
       this.__starts = starts 
    }

    _start(){
        //ejecutara los starts.
        this.__starts 
    }
}
class Process01 extends Process
{
    constructor(a,b){
        this.a = a;
        this.b =b;
        super(this.start)
    }
    start(){
        if(this.a>this.b){    
            this.substraction();
        }else{
            this.addition();
        }
    }  
    addition(){
        this.result= this.a+this.b;
        this.end();
    }  
    substraction(){
        this.result= this.a-this.b;
        this.end();
    }
    end(){
        this.result =result
        return;
    }

}
//callProcess(name,args)
result=callProcess('Process01',[2,4])
