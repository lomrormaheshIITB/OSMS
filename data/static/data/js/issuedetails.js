let ResetErrors = () => {
	$('#div_username').removeClass('has-error');
	$('#div_quantity_issued').removeClass('has-error');
	$('#div_remarks').removeClass('has-error');
	$('#span_username').text('');
	$('#span_quantity_issued').text('');
	$('#span_remarks').text('');
	$('#span_username').text('Select the user...');
	$('#span_quantity_issued').text('Quantity issued to the selected user...');
	$('#span_remarks').text('Reason to issue the spare...');
	$('#span_username').css('color', '#36c6d3');
	$('#span_quantity_issued').css('color', '#36c6d3');
	$('#span_remarks').css('color', '#36c6d3');
}

$(document).ready(() => {
	$('#spare_details input').attr('placeholder', 'NA');
	$('#spare_details input').attr('disabled', 'true');
	$('#spare_details input').css('background-color', 'white');

	// Bind the issue button
	$('#button_issue').click(() => {
		ResetErrors();
		if ($('#id_username').val() == '') {
			$('#div_username').addClass('has-error');
		        $('#id_username').focus();
			$('#span_username').text("Please select a user!");
			$('#span_username').css('color', 'css');
		 }
		else if ($('#id_quantity_issued').val() == 0) {
			$('#div_quantity_issued').addClass('has-error');
		        $('#id_quantity_issued').focus();
			$('#span_quantity_issued').text("Quantity issued must be greater than zero!");
			$('#span_quantity_issued').css('color', 'red');
		 }
		else if ($('#id_remarks').val() == '') {
			$('#div_remarks').addClass('has-error');
		        $('#id_remarks').focus();
			$('#span_remarks').text("Mandatory Field ! Reason to issue!");
			$('#span_remarks').css('color', 'red');
		 }
		  else {
			$('#form_issue').submit();
		}
	});
});