
$(document).ready(() => { 

    let submitForm = () => {
        if ($('#id_password').val() == "") {
            $('#div_password').addClass('has-error');
            $('#id_password').focus();
        }
        else {
            $('#form_manageusers').submit();
        }
    }

    // Submit form using save button
    $('#button_changeaccess').click(() => {
        $("#input_hidden").val('1');
        submitForm();
    
    });

    $('#button_delete').click(() => {  
        $("#input_hidden").val('2');   
        submitForm();
    });

    // Reset the content
    $('#button_cancel').click(() => {
        $('#form_manageusers').trigger("reset");
    });

});