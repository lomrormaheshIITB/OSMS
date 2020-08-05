$(document).ready(() => {
    // Load the equipment class based on the selected spare class
    // Function to get equipment class using ajax
    let GetEquipmentClass = () => {
        let val = $('#id_spare_class').val();
        let url = `${url_getEquipmentClass}${val}`;
        $.ajax({
            url: url,
            type: 'GET',
            success: function(result){
                let html = `<option value="ALL">ALL</option>`;
                result.equipment_class.forEach(e => {
                    html += `<option value="${e}">${e}</option>`;
                });
                $('#id_equipment_class').html(html);
            }
        });
    }
    // Bind the above function
    $('#id_spare_class').change(GetEquipmentClass);
    
    // Submit form using search button
    $('#button_search').click(() => {
        $('#form_search').submit();
    });

    // Reset form using cancel button
    let ResetForm = () => {
        $('#form_search').trigger("reset");
        $('#id_spare_class').val('ALL').change();
    }
    $('#button_cancel').click(ResetForm);
});

$(window).load(() => {
    // Initialize the form
    $('#id_spare_class').val('ALL').change();
    $('#id_equipment_class').val('ALL').change();
});