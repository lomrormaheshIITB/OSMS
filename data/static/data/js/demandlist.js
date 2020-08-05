// Filter array contains the values of the crtical and category options
// filter = [critical, permanent, returnable, consumable]
let filter = ['', 'checked', 'checked', 'checked'];

// Filter based on critcal status
let FilterCritical = (spares) => {
    if ($('#critical').prop("checked") == true){
        filter[0] = 'checked';
        return spares.filter(spare => {return spare.critical === 'True'});
    }
    else {
        filter[0] = '';
        return spares;
    }
};

// Filter based on category
let FilterCategory = (spares) => {
    spares_permanent = [];
    if ($("#permanent").prop("checked") == true){
        filter[1] = 'checked';
        spares_permanent = spares.filter(spare => {return spare.category === 'PERMANENT'});
    }
    else {
        filter[1] = '';
    }

    spares_returnable = [];
    if ($("#returnable").prop("checked") == true){
        filter[2] = 'checked';
        spares_returnable = spares.filter(spare => {return spare.category === 'RETURNABLE'});
    }
    else {
        filter[2] = '';
    }

    spares_consumable = [];
    if ($("#consumable").prop("checked") == true){
        filter[3] = 'checked';
        spares_consumable = spares.filter(spare => {return spare.category === 'CONSUMABLE'});
    }
    else {
        filter[3] = '';
    }

    return spares_consumable.concat(spares_returnable, spares_permanent);
};

// Populate the table with enries
let LoadTable = (init) => {
    // Filter the spares
    let spares = result;
    if (! init) {
        spares = FilterCritical(spares);
        spares = FilterCategory(spares);
    }

    // Destroy the existing datatable
    if ($.fn.DataTable.isDataTable('#sample_1')) {
        $('#sample_1').DataTable().clear().destroy();
        $('#sample_1 tbody').unbind();
    }

    let html = ``;
    for (var i = spares.length - 1; i >= 0; i--) {
        html += `
            <tr class = "table-row">
                <td>${url_demand}${spares[i].pk}/</td>
                <td>${spares[i].pattern_number}</td>
                <td>${spares[i].spare_class}</td>
                <td>${spares[i].equipment_class}</td>                
                <td>${spares[i].description}</td>
                <td>${spares[i].quantity_todemand}</td>
                <td>${spares[i].survey_number}</td>
                <td>${spares[i].survey_remarks}</td>
            </tr>
        `;
    }
    $('#table_body').html(html);
    DataTableCall();
};

// Load the filter buttons${filter[1]}
let LoadFilter = () => {
    let html = `
    <div class="form-group form-md-line-input">
        <div class="row">
            <div class="col-lg-4">
                <div class="row"><div class="col-lg-12">
                    <div class="md-checkbox-inline">
                        <label style="width: 80px;"><strong>Critical</strong></label>
                        <div class="md-checkbox">
                            <input type="checkbox" id="critical" class="md-check" ${filter[0]}>
                            <label for="critical">
                                <span></span>
                                <span class="check"></span>
                                <span class="box"></span>
                            </label>
                        </div>
                    </div>
                </div></div>
            </div>
            <div class="col-lg-8">
                <div class="row" style="float: right;"><div class="col-lg-12">
                    <div class="md-checkbox-inline">
                        <label style="width: 80px;"><strong>Category</strong></label>
                        <div class="md-checkbox">
                            <input type="checkbox" id="permanent" class="md-check" ${filter[1]}>
                            <label for="permanent">
                                <span></span>
                                <span class="check"></span>
                                <span class="box"></span>Permanent</label>
                        </div>
                        <div class="md-checkbox">
                            <input type="checkbox" id="returnable" class="md-check" ${filter[2]}>
                            <label for="returnable">
                                <span></span>
                                <span class="check"></span>
                                <span class="box"></span>Returnable</label>
                        </div>
                        <div class="md-checkbox">
                            <input type="checkbox" id="consumable" class="md-check" ${filter[3]}>
                            <label for="consumable">
                                <span></span>
                                <span class="check"></span>
                                <span class="box"></span>Consumable</label>
                        </div>
                    </div>
                </div></div>
            </div>
        </div>
    </div>
    `;
    $('#filter').html(html);
};

// Assign click events ot filter buttons
let HandleClick = () => {
    $('#critical').click(() => {
        LoadTable(false);
    });
    $('#permanent').click(() => {
        LoadTable(false);
    });
    $('#returnable').click(() => {
        LoadTable(false);
    });
    $('#consumable').click(() => {
        LoadTable(false);
    });
};

// Ajax call to the metronics js file
let DataTableCall = () => {
    $.when(
        $.getScript('/static/data/js/datatable_demandlist.js'),
        $.Deferred(function( deferred ){
            $(deferred.resolve);
        })
    )
    .done(() => {
        LoadFilter();
        HandleClick();
    });
};
