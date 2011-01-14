var opencount = 0;
var working = false;
var $first;
var $card = [];
$(document).ready(function() {
	init();
	
	function init(){
		opencount = 0;
		working = false;
		$('#correct').val('0');
		$('#open').val('0');
		$card = [];

		$('#cards li').each(function(index){
			$card.push($(this));
			$(this).addClass('show');
			$(this).removeClass('hide');
			$(this).removeClass('gone');
			$(this).detach();
		});
		
		$card = shuffle($card);
		
		$.each($card,function(index,value){
			$('#cards').append($(this));
			$(this).fadeIn('fast');
		});
		
		setTimeout(function(){
			$.each($card,function(index,value){
				$(this).removeClass('show');
				$(this).addClass('hide');
			});
		},300);
	}
	
	$('#reset').click(function(){init()});
	
	
	$('#cards li:not(.gone)').click(function(){
		if(!working){
			$('#open').val(parseInt($('#open').val())+1);
			
			if(!$(this).hasClass('hide')){
				$first.removeClass('show');
				$first.addClass('hide');
				opencount = 0;
			}else{
				$(this).addClass('show');
				$(this).removeClass('hide');
				if(opencount == 0){
					$first = $(this);
					opencount = 1;
				}else{
					checkAnswer($(this));
					opencount = 0;
				}
			}
		}
	});
	
	function checkAnswer($obj){
		working = true;
		setTimeout(function(){
			if($obj.attr('data') == $first.attr('data')){
				$('#correct').val(parseInt($('#correct').val())+1);
				$first.addClass('gone');
				$obj.addClass('gone');
				if(parseInt($('#correct').val()) == $card.length / 2){
					alert('You win!');
					init();
				}
			}else{
				$first.addClass('hide');
				$first.removeClass('show');
				$obj.addClass('hide');
				$obj.removeClass('show');
			}
			working = false;
		},1000);
	}
});

shuffle = function(o){ //v1.0
	for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
	return o;
};