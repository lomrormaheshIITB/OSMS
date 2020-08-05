
$(document).ready(() => { 

    // Submit form using save button
    $('#button_user_save').click(() => {        
        $('#form_signupuser').submit();
    });


    // Reset the content
    $('#button_cancel').click(() => {
        $('#form_signupuser').trigger("reset");
        
    });

});