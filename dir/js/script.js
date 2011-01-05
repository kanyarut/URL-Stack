// when html loaded
$(document).ready(function() {
	$.ajax({
	  url: '/category',
	  success: function(data) {
	    $('#category').html(data);
	  }
	});
	
	$.ajax({
	  url: '/weblink',
	  success: function(data) {
	    $('#linkslist').html(data);
	  }
	});
	
	$('a.delete').live('click',function(e){
		e.preventDefault();
		if(confirm('Sure u wanna delete?')){
			$.ajax({
			  url: $(this).attr('href'),
			  success: function(data) {
			    $('#linkslist').html(data);
			  }
			});
		}
		return false;
	});
	
	$('#categorylist li a').live('click',function(e){
		e.preventDefault();
		$('#categorylist li a').removeClass('active');
		$(this).addClass('active');
		$.ajax({
		  url: $(this).attr('href'),
		  success: function(data) {
		    $('#linkslist').html(data);
		  }
		});
		return false;
	});
	
	$('#search').live('submit',function(e){
		e.preventDefault();
		$.ajax({
			url: "/weblink/search",
			type: "POST",
			data: ($(this).serialize()),
			success: function(msg){
				$('#linkslist').html(msg);
			}
		});
		return false;
	});
	
	$('#addcategory').live('submit',function(e){
		e.preventDefault();
		$.ajax({
			url: "/category/add",
			type: "POST",
			data: ($(this).serialize()),
			success: function(msg){
				$('#category').html(msg);
			}
		});
		return false;
	});
});

function saveReadingProgress(key,percent,oldp){
	if(oldp < percent){
		$.ajax({
		  url: '/weblink/read',
		  type: "POST",
		  data: 'key='+key+'&percent='+percent,
		  success: function(data) {
		   //$('#linkslist').html(data);
		  }
		});
	}
}
// when all page elements loaded
$(window).load(function() {

});
