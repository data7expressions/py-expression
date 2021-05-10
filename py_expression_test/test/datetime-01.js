//https://www.w3schools.com/js/js_date_methods.asp
now = now();
now = addTime();
milliseconds= getMilliseconds(now);
seconds = getSeconds(now);
minutes = getMinutes(now);
hours = getHours(now);
day = getDay(now);
date = getDate(now);
month = getMonth(now);
year = getFullYear(now); //getYear

//https://www.w3schools.com/js/js_dates.asp
date= Date()
date2= Date(year, month, day, hours, minutes, seconds, milliseconds)
date3= Date(122132323) //Date(milliseconds)
date4 = Date("2015-03-25") //Date(date string)
//https://www.w3schools.com/js/js_date_formats.asp
date5 = Date("2015");
date6 = Date("2015-03-25T12:00:00Z");
date7=  Date("2015-03-25T12:00:00-06:30");

//https://www.w3schools.com/js/js_date_methods_set.asp
setDate(date,22);
setFullYear(date,2020);
setHours(date,18);
setMilliseconds(date,600);
setMinutes(date,45);
setMonth(date,3);
setSeconds(date,44);
setTime(date,4343332);

addDate(date,22);
addYear(date,2020);
addHours(date,18);
addMilliseconds(date,600);
addMinutes(date,45);
addMonth(date,3);
addSeconds(date,44);
addTime(date,4343332);

date10=  Date("2015-03-25T12:00:00-06:30");
date11= Date();

diffDays(date10,date11);
diffDay(date10,date11);
diffDate(date10,date11);
diffYear(date10,date11);
diffHours(date10,date11);
diffilliseconds(date10,date11);
diffMinutes(date10,date11);
diffMonth(date10,date11);
diffSeconds(date10,date11);
diffTime(date10,date11);