/**
 * twitter.relative.time.js 0.2.0
 * Copyright (c) 2013 Keita Mori
 * https://github.com/dforest/twitter-relative-time-js
 *
 * Includes data.extentions.js
 * Copyright (c) 2009 James F. Herdman
 * https://github.com/jherdman/javascript-relative-time-helpers
 *
 * Released under the MIT License.
 */
Date.prototype.toTwitterRelativeTime=function(){var d="def",g=function(a,b){var c=e[d][b];"month"===b?(c=c[a.getMonth()],a=a.getDate()):"now"!==b&&(c=1===a?e[d][b].one:e[d][b].other);return c.replace("%n",a+"")},f={now:1,second:1E3,minute:60,hour:60},e={def:{now:"Now",second:{one:"%ns",other:"%ns"},minute:{one:"%nm",other:"%nm"},hour:{one:"%nh",other:"%nh"},month:"%n Jan;%n Feb;%n Mar;%n Apr;%n May;%n June;%n July;%n Aug;%n Sept;%n Oct;%n Nov;%n Dec".split(";")},en:{now:"Now",second:{one:"%n second ago",
other:"%n seconds ago"},minute:{one:"%n minute ago",other:"%n minutes ago"},hour:{one:"%n hour ago",other:"%n hours ago"},month:"%n January;%n February;%n March;%n April;%n May;%n June;%n July;%n August;%n September;%n October;%n November;%n December".split(";")},ja:{now:"\u4eca",second:{one:"%n\u79d2\u524d",other:"%n\u79d2\u524d"},minute:{one:"%n\u5206\u524d",other:"%n\u5206\u524d"},hour:{one:"%n\u6642\u9593\u524d",other:"%n\u6642\u9593\u524d"},month:"1\u6708%n\u65e5 2\u6708%n\u65e5 3\u6708%n\u65e5 4\u6708%n\u65e5 5\u6708%n\u65e5 6\u6708%n\u65e5 7\u6708%n\u65e5 8\u6708%n\u65e5 9\u6708%n\u65e5 10\u6708%n\u65e5 11\u6708%n\u65e5 12\u6708%n\u65e5".split(" ")},
ar:{now:"\u0627\u0644\u0622\u0646.",second:{one:"\u0645\u0646\u0630 \u200f%n \u062b\u0627\u0646\u064a\u062a\u064a\u0646",other:"\u0645\u0646\u0630 \u200f%n\u200f \u062b\u0627\u0646\u064a\u062a\u064a\u0646"},minute:{one:"\u0645\u0646\u0630 %n \u062f\u0642\u0627\u0626\u0642",other:"\u0645\u0646\u0630 %n \u062f\u0642\u0627\u0626\u0642"},hour:{one:"\u0645\u0646\u0630 %n \u0633\u0627\u0639\u0627\u062a",other:"\u0645\u0646\u0630 %n \u0633\u0627\u0639\u0627\u062a"},month:"%n \u064a\u0646\u0627\u064a\u0631;%n \u0641\u0628\u0631\u0627\u064a\u0631;%n \u0645\u0627\u0631\u0633;%n \u0623\u0628\u0631\u064a\u0644;%n \u0645\u0627\u064a\u0648;%n \u064a\u0648\u0646\u064a\u0648;%n \u064a\u0648\u0644\u064a\u0648;%n \u0623\u063a\u0633\u0637\u0633;%n \u0633\u0628\u062a\u0645\u0628\u0631;%n \u0623\u0643\u062a\u0648\u0628\u0631;%n \u0646\u0648\u0641\u0645\u0628\u0631;%n \u062f\u064a\u0633\u0645\u0628\u0631".split(";")},
de:{now:"Jetzt",second:{one:"Vor %n Sekunde",other:"vor %n Sekunden"},minute:{one:"Vor %n Minute",other:"vor %n Minuten"},hour:{one:"Vor %n Stunde",other:"vor %n Stunden"},month:"%n Januar;%n Februar;%n M\u00e4rz;%n April;%n Mai;%n Juni;%n Juli;%n August;%n September;%n Oktober;%n November;%n Dezember".split(";")},es:{now:"Ahora",second:{one:"%n segundo atr\u00e1s",other:"%n segundos atr\u00e1s"},minute:{one:"%n minuto atr\u00e1s",other:"%n minutos atr\u00e1s"},hour:{one:"%n hora atr\u00e1s",other:"%n horas atr\u00e1s"},
month:"%n Enero;%n Febrero;%n Marzo;%n Abril;%n Mayo;%n Junio;%n Julio;%n Agosto;%n Septiembre;%n Octubre;%n Noviembre;%n Diciembre".split(";")},fr:{now:"Maintenant",second:{one:"Il y a %n seconde",other:"il y a %n secondes"},minute:{one:"Il y a %n minute",other:"il y a %n minutes"},hour:{one:"Il y a %n heure",other:"il y a %n heures"},month:"%n Janvier;%n F\u00e9vrier;%n Mars;%n Avril;%n Mai;%n Juin;%n Juillet;%n Ao\u00fbt;%n Septembre;%n Octobre;%n Novembre;%n D\u00e9cembre".split(";")},hi:{now:"\u0905\u092c",
second:{one:"%n \u0938\u0947\u0915\u0902\u0921 \u092a\u0939\u0932\u0947",other:"%n \u0938\u0947\u0915\u0902\u0921 \u092a\u0939\u0932\u0947"},minute:{one:"%n \u092e\u093f\u0928\u091f \u092a\u0939\u0932\u0947",other:"%n \u092e\u093f\u0928\u091f \u092a\u0939\u0932\u0947"},hour:{one:"%n \u0918\u0902\u091f\u0947 \u092a\u0939\u0932\u0947",other:"%n \u0918\u0902\u091f\u0947 \u092a\u0939\u0932\u0947"},month:"%n \u091c\u0928\u0935\u0930\u0940;%n \u092b\u0930\u0935\u0930\u0940;%n \u092e\u093e\u0930\u094d\u091a;%n \u0905\u092a\u094d\u0930\u0948\u0932;%n \u092e\u0908;%n \u091c\u0942\u0928;%n \u091c\u0941\u0932\u093e\u0908;%n \u0905\u0917\u0938\u094d\u0924;%n \u0938\u093f\u0924\u0902\u092c\u0930;%n \u0905\u0915\u094d\u091f\u0942\u092c\u0930;%n \u0928\u0935\u0902\u092c\u0930;%n \u0926\u093f\u0938\u0902\u092c\u0930".split(";")},
id:{now:"Sekarang",second:{one:"%n detik yang lalu",other:"%n detik yang lalu"},minute:{one:"%n menit yang lalu",other:"%n menit yang lalu"},hour:{one:"%n jam yang lalu",other:"%n jam yang lalu"},month:"%n Januari;%n Februari;%n Maret;%n April;%n Mei;%n Juni;%n Juli;%n Agustus;%n September;%n Oktober;%n November;%n Desember".split(";")},it:{now:"Ora",second:{one:"%n secondo fa",other:"%n secondi fa"},minute:{one:"%n minuto fa",other:"%n minuti fa"},hour:{one:"%n ora fa",other:"%n ore fa"},month:"%n Gennaio;%n Febbraio;%n Marzo;%n Aprile;%n Maggio;%n Giugno;%n Luglio;%n Agosto;%n Settembre;%n Ottobre;%n Novembre;%n Dicembre".split(";")},
ko:{now:"\uc9c0\uae08",second:{one:"%n\ucd08 \uc804",other:"%n\ucd08 \uc804"},minute:{one:"%n\ubd84 \uc804",other:"%n\ubd84 \uc804"},hour:{one:"%n\uc2dc\uac04 \uc804",other:"%n\uc2dc\uac04 \uc804"},month:"1\uc6d4%n\uc77c 2\uc6d4%n\uc77c 3\uc6d4%n\uc77c 4\uc6d4%n\uc77c 5\uc6d4%n\uc77c 6\uc6d4%n\uc77c 7\uc6d4%n\uc77c 8\uc6d4%n\uc77c 9\uc6d4%n\uc77c 10\uc6d4%n\uc77c 11\uc6d4%n\uc77c 12\uc6d4%n\uc77c".split(" ")},ms:{now:"sekarang",second:{one:"%n saat yang lalu",other:"%n saat yang lalu"},minute:{one:"%n minit yang lalu",
other:"%n minit yang lalu"},hour:{one:"%n jam yang lalu",other:"%n jam yang lalu"},month:"%n Januari;%n Februari;%n Mac;%n April;%n Mei;%n Jun;%n Julai;%n Ogos;%n September;%n Oktober;%n November;%n Disember".split(";")},pt:{now:"Agora",second:{one:"%n segundo atr\u00e1s",other:"%n segundos atr\u00e1s"},minute:{one:"%n minuto atr\u00e1s",other:"%n minutos atr\u00e1s"},hour:{one:"%n hora atr\u00e1s",other:"%n horas atr\u00e1s"},month:"%n Janeiro;%n Fevereiro;%n Mar\u00e7o;%n Abril;%n Maio;%n Junho;%n Julho;%n Agosto;%n Setembro;%n Outubro;%n Novembro;%n Dezembro".split(";")},
ru:{now:"\u0441\u0435\u0439\u0447\u0430\u0441",second:{one:"%n \u0441\u0435\u043a\u0443\u043d\u0434\u0443 \u043d\u0430\u0437\u0430\u0434",other:"%n \u0441\u0435\u043a\u0443\u043d\u0434 \u043d\u0430\u0437\u0430\u0434"},minute:{one:"%n \u043c\u0438\u043d\u0443\u0442\u0443 \u043d\u0430\u0437\u0430\u0434",other:"%n \u043c\u0438\u043d\u0443\u0442 \u043d\u0430\u0437\u0430\u0434"},hour:{one:"%n \u0447\u0430\u0441 \u043d\u0430\u0437\u0430\u0434",other:"%n \u0447\u0430\u0441\u043e\u0432 \u043d\u0430\u0437\u0430\u0434"},
month:"%n \u044f\u043d\u0432\u0430\u0440\u044c;%n \u0444\u0435\u0432\u0440\u0430\u043b\u044c;%n \u043c\u0430\u0440\u0442;%n \u0430\u043f\u0440\u0435\u043b\u044c;%n \u041c\u0430\u044f;%n \u0438\u044e\u043d\u044c;%n \u0438\u044e\u043b\u044c;%n \u0430\u0432\u0433\u0443\u0441\u0442;%n \u0441\u0435\u043d\u0442\u044f\u0431\u0440\u044c;%n \u043e\u043a\u0442\u044f\u0431\u0440\u044c;%n \u043d\u043e\u044f\u0431\u0440\u044c;%n \u0434\u0435\u043a\u0430\u0431\u0440\u044c".split(";")},tr:{now:"\u015fimdi",second:{one:"%n saniye \u00f6nce",
other:"%n saniye \u00f6nce"},minute:{one:"%n dakika \u00f6nce",other:"%n dakika \u00f6nce"},hour:{one:"%n saat \u00f6nce",other:"%n saat \u00f6nce"},month:"%n Ocak;%n \u015eubat;%n Mart;%n Nisan;%n May\u0131s;%n Haziran;%n Temmuz;%n A\u011fustos;%n Eyl\u00fcl;%n Ekim;%n Kas\u0131m;%n Aral\u0131k".split(";")},"zh-CN":{now:"\u73b0\u5728",second:{one:"%n\u79d2\u949f\u524d",other:"%n\u79d2\u949f\u524d"},minute:{one:"%n\u5206\u949f\u524d",other:"%n\u5206\u949f\u524d"},hour:{one:"%n\u5c0f\u65f6\u524d",
other:"%n\u5c0f\u65f6\u524d"},month:"1\u6708%n\u65e5 2\u6708%n\u65e5 3\u6708%n\u65e5 4\u6708%n\u65e5 5\u6708%n\u65e5 6\u6708%n\u65e5 7\u6708%n\u65e5 8\u6708%n\u65e5 9\u6708%n\u65e5 10\u6708%n\u65e5 11\u6708%n\u65e5 12\u6708%n\u65e5".split(" ")},"zh-TW":{now:"\u73fe\u5728",second:{one:"%n\u79d2\u9418\u524d",other:"%n\u79d2\u9418\u524d"},minute:{one:"%n\u5206\u9418\u524d",other:"%\u5206\u9418\u524d"},hour:{one:"%n\u5c0f\u6642\u524d",other:"%n\u5c0f\u6642\u524d"},month:"1\u6708%n\u65e5 2\u6708%n\u65e5 3\u6708%n\u65e5 4\u6708%n\u65e5 5\u6708%n\u65e5 6\u6708%n\u65e5 7\u6708%n\u65e5 8\u6708%n\u65e5 9\u6708%n\u65e5 10\u6708%n\u65e5 11\u6708%n\u65e5 12\u6708%n\u65e5".split(" ")}};
return function(a){void 0!==a&&e.hasOwnProperty(a)&&(d=a);a=new Date-this;a=Math.abs(a);var b="now",c;for(c in f){if(a<f[c])break;b=c;a/=f[c]}if("hour"===b&&1<=a/24)return g(this,"month",!0);a=Math.floor(a);return g(a,b)}}();
