// Reset the errors
let ResetErrors = () => {
	$('#div_demand_number').removeClass('has-error');
	$('#div_quantity_demanded').removeClass('has-error');
	$('#span_demand_number').text('');
	$('#span_quantity_demanded').text('');
	$('#span_demand_date').text('Demand voucher date...');
	$('#span_demand_date').css('color', '#36c6d3');
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
	return `${year}-${month}-${day}T00:00Z`;
};

$(document).ready(() => {
	$('#spare_details input').attr('placeholder', 'NA');
	$('#spare_details input').attr('disabled', 'true');
	$('#spare_details input').css('background-color', 'white');

	// Bind the issue button
	$('#button_save').click(() => {
		// console.log("hi world");
		ResetErrors();
		if ($('#id_quantity_demanded').val() == 0) {
			$('#div_quantity_demanded').addClass('has-error');
			$('#id_quantity_demanded').focus();
			$('#span_quantity_demanded').text('Must be greated than zero!');
		}
		else if ($('#id_demand_number').val() == '') {
			$('#div_demand_number').addClass('has-error');
			$('#id_demand_number').focus();
			$('#span_demand_number').text('Mandatory field!');
		}
		else if (parseInt($('#id_quantity_demanded').val()) > parseInt($('#id_quantity_todemand').val())) {
			$('#div_quantity_demanded').addClass('has-error');
			$('#id_quantity_demanded').focus();
			$('#span_quantity_demanded').text('Value greater than quantity due for demand!');
		}
		else if ($('#id_demand_date').val() == '') {
			$('#span_demand_date').text('Demand voucher date is a mandatory field!');
			$('#span_demand_date').css('color', 'red');
		}
		else if ($('#id_remarks').val() == '') {
			$('#div_remarks').addClass('has-error');
			$('#id_remarks').focus();
			$('#span_remarks').text('Mandatory field! Kindly Enter demanded by whom and purpose of demanding in brief')
		}
		else {
			$('#form_demand').submit();
			// console.log("form submitted");
		}
		
	});
});

$(window).load(() => {
	// Initialize the current date to date picker
	$('#id_demand_date').data('date', CurrentDate());
	$('#id_demand_date').css('background-color', 'white');
});