i = 0;
signal =listeners(["signal_1","signal_2"],now())
switch(signal){
    case "signal_1": 
        i=1;
    case "signal_2":
        i=2; 
    case "time":
        i=3;       
}