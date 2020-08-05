// Reset the errors
let ResetErrors = () => {
	$('#div_receipt_number').removeClass('has-error');
	$('#div_quantity_received').removeClass('has-error');
	$('#span_receipt_number').text('');
	$('#span_quantity_received').text('');
	$('#span_receive_date').text('Receive voucher date...');
	$('#span_receive_date').css('color', '#36c6d3');

};

// Current date
let CurrentDate = () => {
	let date = new Date();
	let year =  date.getFullYear();
	let month = date.getMonth() + 1;
	if (month < 10) {
		month = `0${month}`;
	}
	let day = date.getDate();
	if (day < 10) {
		day = `0${day}`;
	}
	return `${year}-${month}-${day}T00:00:001Z`;
};

$(document).ready(() => {
	$('#spare_details input').attr('placeholder', 'NA');
	$('#spare_details input').attr('disabled', 'true');
	$('#spare_details input').css('background-color', 'white');

	// Bind the issue button
	$('#button_save').click(() => {
		ResetErrors();
		if ($('#id_receipt_number').val() == '') {
			$('#div_receipt_number').addClass('has-error');
			$('#id_receipt_number').focus();
			$('#span_receipt_number').text('Mandatory field!');
		}
		else if ($('#id_quantity_received').val() == 0) {
			$('#div_quantity_received').addClass('has-error');
			$('#id_quantity_received').focus();
			$('#span_quantity_received').text('Must be greated than zero!');
		}
		else if (parseInt($('#id_quantity_received').val()) > parseInt($('#id_quantity_toreceive').val())) {
			$('#div_quantity_received').addClass('has-error');
			$('#id_quantity_received').focus();
			$('#span_quantity_received').text('Value greater than quantity due to be received!');
		}
		else if ($('#id_receive_date').val() == '') {
			$('#span_receive_date').text('Receive voucher date is a mandatory field!');
			$('#span_receive_date').css('color', 'red');
		}
		else if ($('#id_remarks').val() == '') {
			$('#div_remarks').addClass('has-error');
			$('#id_remarks').focus();
			$('#span_remarks').text('Mandatory field! Kindly Enter Received by whom and purpose of receiving in brief')
		}
		else {
			$('#form_receive').submit();
		}
	});
});

$(window).load(() => {
	// Initialize the current date to date picker
	$('#id_receive_date').data('date', CurrentDate());
	$('#id_receive_date').css('background-color', 'white');
	
});