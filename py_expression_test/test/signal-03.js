i = 0;
signal =listen(["signal_1","signal_2"], addTime(now(),time(2,10,30)))
switch(signal){
    case "signal_1": 
        i=1;
    case "signal_2":
        i=2; 
    case "time":
        i=3;       
}
