i = 0;
signal =listen(["signal_1"],addTime(now(),time("2:10:30")));
if (signal=="signal_1"){
    i = 1;
}else if (signal=="time") {
    i = 2;
}
wait(now());
i = 3;
listen(["signal_2"]);
i = 4;