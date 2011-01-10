$(document).ready(function(){
	if(read>0 && $(document).height() > $(window).height()){
		gotoRead();
	}
	
	$('#gotoread').click(function(){gotoRead()});
	
	function gotoRead(){
		var scrollto = (($(document).height()*read)/100) - $(window).height();
		$(window).scrollTop(scrollto);
		//$('body','html').animate({scrollTop: scrollto+'px'});
	}

	if($(document).height() <= $(window).height()){
		parent.childScrollHandler(key,100,read); 
	}else{
		parent.childScrollHandler(key,1,read); 
		$(document).bind('scroll', function(ev){ 
			var bottom = $(window).height() + $(window).scrollTop(); 
			var height = $(document).height();
			var percentage = Math.round(100*bottom/height); 
			parent.childScrollHandler(key,percentage,read); 
		});
	}
});