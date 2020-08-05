$(document).ready(() => {
	$('input').attr('placeholder', 'NA');
	$('input').attr('disabled', 'true');
	$('.textarea').attr('disabled', 'true');
	$('input').css('background-color', 'white');
	$('.textarea').css('background-color', 'white');

	
	//   $(document).keypress(function(event) { 
		

	// 	if (event.keyCode == 37) { 
	// 		$("#button_left").click(); 
	// 	} 
	// 	if (event.keyCode == 39) { 
	// 		$("#button_right").click(); 
	// 	} 
		$(window).keypress((e) => {
			if (e.which == 13) { 
				$("#button_issue").click(); 
			} 
		});

	}); 















