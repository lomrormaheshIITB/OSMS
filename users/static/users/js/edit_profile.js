$(document).ready(() => { 
    // Submit form using save button
    $('#btn_save_changes').click(() => {
        $('#form_profile').submit();
    });

    // Reset the content
    $('#button_cancel').click(() => {
        $('#form_profile').trigger("reset");
        
    });

    // Submit form using password save button
    $('#btn_change_password').click(() => {        
        $('#form_password').submit();
    });
    
    $('#btn_cancel_password').click(() => {
        $('#form_password').trigger("reset");     
    });

    // Check if the new passwords are same
    let checkPassword = () => {
        return ($('#id_password1').val() === $('#id_password2').val());
    };

    let inputHandler = (e) => {
        if (checkPassword()) {
            $('#password_error').text('');
        }
        else {
            $('#password_error').text('Passwords do not match.');
            $('#password_error').css('color', 'red');
        }
    }

    $('#id_password1').on('input', inputHandler);
    $('#id_password2').on('input', inputHandler);
});