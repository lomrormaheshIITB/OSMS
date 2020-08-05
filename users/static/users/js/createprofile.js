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

    // Submit form using save button
    $('#button_profile_save').click(() => {        
        $('#form_profile').submit();
    });


    // Reset the content
    $('#button_cancel').click(() => {
        $('#form_profile').trigger("reset");
        
    });

});


$(window).load(() => {
	// Initialize the current date to date picker
	$('#id_ship_joining_date').data('date', CurrentDate());
	$('#id_ship_joining_date').css('background-color', 'white');

});