$(document).ready(() => {
	$('#spare_details input').attr('placeholder', 'NA');
	$('#spare_details input').attr('disabled', 'true');
	$('#spare_details input').css('background-color', 'white');

	// Bind the issue button
	$('#button_return').click(() => {
		$('#form_return').submit();
	});
});