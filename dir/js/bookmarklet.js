a=document.createElement('a');
a.setAttribute('id', 'close');
a.innerHTML = 'x';
a.setAttribute('style', 'height: 16px;width:16px;line-height:14px;text-align:center; border-radius:8px; -moz-border-radius:8px; border: 1px solid #EEE;float:right;display:block;color:#FFF;font-size:14px;text-decoration:none;cursor: pointer;');

h=document.createElement('a');
h.setAttribute('href', 'http://urlstack.appspot.com/');
h.innerHTML = 'URL Stack';
h.setAttribute('style', 'color: #FFF;float:left;padding:3px;');

i=document.createElement('iframe');
i.setAttribute('name', 'later');
i.setAttribute('id', 'later');
i.setAttribute('src', 'http://urlstack.appspot.com/weblink/add?rel='+document.location.href);
//i.setAttribute('src', 'http://localhost:8082/weblink/add?rel='+document.location.href);
i.setAttribute('style', 'border:0;clear:both;float:left;');
i.setAttribute('width', '250px');
i.setAttribute('height', '210px');
/*
i.addEventListener("load", function(event) { 
	i.setAttribute('width', (i.scrollWidth+30)+'px');
	i.setAttribute('height', (i.scrollHeight+60)+'px');
}, false);
*/
d = document.createElement('div');
d.setAttribute('id', 'laterWrapper');
d.setAttribute('style', 'font: 12px/16px "Lucida Sans Unicode", "Lucida Grande", sans-serif;position:fixed; z-index: 100;left:3px;top:3px; border-radius:5px;-moz-border-radius:5px;background: #3f91ce;width:auto;height:auto;overflow:hidden;padding:5px;-webkit-box-shadow: 2px 2px 4px #888;-moz-box-shadow: 2px 2px 4px #888;box-shadow: 2px 2px 4px #888;');
d.appendChild(h);
d.appendChild(a);
d.appendChild(i);
document.body.appendChild(d);

a.addEventListener('click',function(){
	document.body.removeChild(d)
},false)