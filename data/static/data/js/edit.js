// Load the equipment class based on the selected spare class
// Function to get equipment class using ajax
let GetEquipmentClass = () => {
    let val = $('#id_spare_class').val();
    let eq_val = $('#id_equipment_class').val();
    let url = `${url_getEquipmentClass}${val}/`;
    $.ajax({
        url: url,
        type: 'GET',
        success: function(result){
            if (result.equipment_class.length == 0) {
                let message = `No equipment class exists for ${val}.\nPlease create a new equipment class.\n`; 
                alert(message);
                window.location = url_addMiscellaneous;
            }

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
        $('#form_edit').submit();
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
