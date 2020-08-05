// Reset the errors
let ResetErrors = () => {
	$('#div_survey_number').removeClass('has-error');
	$('#div_quantity_surveyed').removeClass('has-error');
	$('#span_survey_number').text('');
	$('#span_quantity_surveyed').text('');
	$('#span_survey_number_date').text('Survey number generation date...');
	$('#span_survey_report_date').text('Survey report generation date...');
	$('#span_survey_number_date').css('color', '#36c6d3');
	$('#span_survey_report_date').css('color', '#36c6d3');

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
		ResetErrors();
		if ($('#id_survey_number').val() == '') {
			$('#div_survey_number').addClass('has-error');
			$('#id_survey_number').focus();
			$('#span_survey_number').text('Mandatory field!');
		}
		else if ($('#id_quantity_surveyed').val() == 0) {
			$('#div_quantity_surveyed').addClass('has-error');
			$('#id_quantity_surveyed').focus();
			$('#span_quantity_surveyed').text('Must be greated than zero!');
		}
		else if (parseInt($('#id_quantity_surveyed').val()) > parseInt($('#id_quantity_tosurvey').val())) {
			$('#div_quantity_surveyed').addClass('has-error');
			$('#id_quantity_surveyed').focus();
			$('#span_quantity_surveyed').text('Value greater than quantity due for survey!');
		}
		else if ($('#id_survey_number_date').val() == '') {
			$('#span_survey_number_date').text('Survey number generation date is a mandatory field!');
			$('#span_survey_number_date').css('color', 'red');
		}
		else if ($('#id_survey_report_date').val() == '') {
			$('#span_survey_report_date').text('Survey report generation date is a mandatory field!');
			$('#span_survey_report_date').css('color', 'red');
		}
		else if ($('#id_remarks').val() == '') {
			$('#div_remarks').addClass('has-error');
			$('#id_remarks').focus();
			$('#span_remarks').text('Mandatory field! Kindly enter surveyed by whom and purpose of survey in brief')
		}
		else {			
			$('#form_survey').submit();
		}
	});
	// Bind the bypass button
	$('#button_bypass').click(() => {
		var result = confirm('Are you sure survey details of the spare to be ignored? Click yes to confirm');
            if (result == true) { 
                $.ajax({
					url: url_surveybypass,
					type: 'GET',        
				});
				return true;
			} 
			else { 
                return false;
            } 
		
		
	});
});

$(window).load(() => {
	// Initialize the current date to date picker
	$('#id_survey_number_date').data('date', CurrentDate());
	$('#id_survey_report_date').data('date', CurrentDate());
	$('#id_survey_number_date').css('background-color', 'white');
	$('#id_survey_report_date').css('background-color', 'white');
});