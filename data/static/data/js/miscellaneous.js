// Load the equipment class based on the selected spare class
$(document).ready(() => {
    // Reset form using cancel button
    let ResetForm = (id) => {
        $(`#form${id}`).trigger("reset");
    }
    $('#button_cancel1').click(() => {ResetForm('1');});
    $('#button_cancel2').click(() => {ResetForm('2');});
    $('#button_cancel3').click(() => {ResetForm('3');});
    $('#button_cancel4').click(() => {ResetForm('4');});
    $('#button_cancel5').click(() => {ResetForm('5');});

    // Get the spare classes asynchronously
    let GetSpareClass = () => {
        let url = `${url_getSpareClass}`;
        $.ajax({
            url: url,
            type: 'GET',
            success: function(result){
                html = '';
                result.spare_class.forEach(e => {
                    html += `<option value="${e}">${e}</option>`;
                });
                $('#form3 #id_spare_class').html(html);
            }
        });
    }

    // Submit form using ajax
    let SubmitForm = (id, name, spare_class) => {
        $.ajax({
            type: "POST",
            url: url_AddMiscellaneous,
            data: {
                'form_id': id,
                'name': name,
                'spare_class': spare_class,
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
            },
            success: (data) => {
                alert(data.message);
                ResetForm(id);
                if (id == '1') {
                    // Load the newly added spare class to the equipment class form
                    GetSpareClass();
                }
            },
        });
    };

    $('#button_save1').click(() => {SubmitForm('1', $('#form1 input[id="id_name"]').val());});
    $('#button_save2').click(() => {SubmitForm('2', $('#form2 input[id="id_name"]').val());});
    $('#button_save3').click(() => {SubmitForm('3', $('#form3 input[id="id_name"]').val(), $('#form3 select[id="id_spare_class"]').val());});
    $('#button_save4').click(() => {SubmitForm('4', $('#form4 input[id="id_name"]').val());});
    $('#button_save5').click(() => {SubmitForm('5', $('#form5 input[id="id_name"]').val());});

});

