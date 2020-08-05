// Load the equipment class based on the selected spare class
// Function to get equipment class using ajax
let GetEquipmentClass = () => {
    let val = $('#id_spare_class').val();
    let eq_val = $('#id_equipment_class').val();
    let url = `${url_getEquipmentClass}${val}`;
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result){
            let html = ``;
            result.equipment_class.forEach(e => {
                html += `<option value="${e}">${e}</option>`;
            });
            $('#id_equipment_class').html(html);
        }
    });
};

$(document).ready(() => {
    // Bind the above function
    $('#id_spare_class').change(() => {
        GetEquipmentClass();
    });

    // Submit form using save button
    $('#button_save').click(() => {
        if ($('#id_pattern_number').val() == ''){
            $('#div_pattern_number').addClass('has-error');
            $('#id_pattern_number').focus();
            $('#span_pattern_number').text('Mandatory field!')
        }
        else if ($('#id_reference').val() == ''){
            $('#div_reference').addClass('has-error');
            $('#id_reference').focus();
        }
        else if ($('#id_quantity_authorised').val() == '0'){
            $('#div_quantity_authorised').addClass('has-error');
            $('#id_quantity_authorised').focus();
            $('#span_quantity_authorised').text('Must be greater than zero!')
        }
        else if ($('#id_description').val() == ''){
            $('#div_description').addClass('has-error');
            $('#id_description').focus();
            $('#span_description').text('Mandatory field!')
        }
        else {
            $('#form_add').submit();
        }

    });

    // Reset the form using the cancel button
    $('#button_cancel').click(() => {
        $('#form_add').trigger('reset');
    });

    // Scale the loaded image to match the div size
    $('#id_image').change(() => {
        setTimeout(() => {
            $('.fileinput-preview img').width('100%');
            $('.fileinput-preview img').height('100%');
        }, 100);
    });

    // Remove the existing image
    $('#button_remove').click(() => {
        $('#img_spare').attr('src', url_emptyImage);
        
    });

});

$(window).load(() => {
    GetEquipmentClass();
});
