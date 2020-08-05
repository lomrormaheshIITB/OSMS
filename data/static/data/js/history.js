// Currently active tab
let currentTab = undefined;

// Object to convert months to numbers
let Months = {
    "January" : '01',
    "February" : '02',
    "March" : '03',
    "April" : '04',
    "May" : '05',
    "June" : '06',
    "July" : '07',
    "August" : '08',
    "September" : '09',
    "October" : '10',
    "November" : '11',
    "December" : '12'
}

// Function to convert date to specified format
let ConvertDate = (date) => {
    year = date[2];
    month = Months[date[0]];
    day = date[1];
    if (day.length == 2) {
        return `${year}-${month}-0${day.slice(0,1)}`;
    }
    else {
        return `${year}-${month}-${day.slice(0,2)}`;
    }
};

// Function to sort according to current date
let SortDate = (data) => {
    let daterange = $('#span_date').text().split("-");
    let startDate = `${ConvertDate(daterange[0].split(" ").slice(0, 3))}T00:00`;
    let endDate = `${ConvertDate(daterange[1].split(" ").slice(1, 4))}T23:59`;

    let result = [];
    for (var i = data.length - 1; i >= 0; i--) {
        if (data[i].date >= startDate && data[i].date <= endDate) {
            result.push(data[i]);
        }
    }
    return result;
};

// Load issue table on click
let LoadIssue = (history_issue, history_return) => {
    currentTab = 'history_issue';
    let table =         `
        <table class="table table-striped table-bordered table-hover dt-responsive" width="100%" id="sample_3" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th class="all">Action</th>
                    <th class="all">Pattern Number</th>
                    <th class="all">Class of Equipment</th>
                    <th class="all">Spare description</th>
                    <th class="min-phone-l">Username</th>
                    <th class="min-tablet">Quantity</th>
                    <th class="none">Issue Date</th>
                    <th class="none">Reason</th>
                </tr>
            </thead>
            <tbody>
        `;

    let e = history_issue;
    for (var i = e.length - 1; i >= 0; i--) {
        table += `
            <tr>
                <td>Issue</td>
                <td>${e[i].pattern_number}</td>
                <td>${e[i].equipment_class}</td>
                <td>${e[i].description}</td>                
                <td>${e[i].username}</td>
                <td>${e[i].quantity}</td>
                <td>${e[i].date}</td>
                <td>${e[i].remarks}</td>
            </tr>`;
    }

    e = history_return;
    for (var i = e.length - 1; i >= 0; i--) {
        table += `
            <tr>
                <td>Return</td>
                <td>${e[i].pattern_number}</td>
                <td>${e[i].equipment_class}</td>
                <td>${e[i].description}</td>
                <td>${e[i].username}</td>
                <td>${e[i].quantity}</td>
                <td>${e[i].date}</td>
                <td>${e[i].remarks}</td>
            </tr>`;
    }

    table +=`</tbody></table>`;

    $('#table_head').html('Spares Issued / Returned');
    $('#table').html(table);
    $.ajax({
        url: "/static/assets/pages/scripts/table-datatables-responsive.js",
        dataType: "script",
        success: () => {}
    });
};

$('#history_issue').click(() => {
    LoadIssue(SortDate(data.history_issue), SortDate(data.history_return));
});


// Load survey details in the table on click
let LoadSurvey = (history_survey) => {
    currentTab = 'history_survey';
    let table = 
        `
        <table class="table table-striped table-bordered table-hover dt-responsive" width="100%" id="sample_3" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th class="all">Pattern Number</th>
                    <th class="all">Class of Equipment</th>
                    <th class="all">Spare description</th>
                    <th class="min-phone-l">Survey Number</th>
                    <th class="min-tablet">Quantity Surveyed</th>
                    <th class="none">Survey Date</th>
                    <th class="none">Remarks</th>
                </tr>
            </thead>
            <tbody>
        `;

    let e = history_survey;
    for (var i = e.length - 1; i >= 0; i--) {
        table += `
            <tr>
                <td>${e[i].pattern_number}</td>
                <td>${e[i].equipment_class}</td>
                <td>${e[i].description}</td>  
                <td>${e[i].survey_number}</td>
                <td>${e[i].quantity}</td>
                <td>${e[i].date}</td>
                <td>${e[i].remarks}</td>
            </tr>`;
    }

    table +=`</tbody></table>`;

    $('#table_head').html('Spares Surveyed');
    $('#table').html(table);
    $.ajax({
        url: "/static/assets/pages/scripts/table-datatables-responsive.js",
        dataType: "script",
        success: () => {}
    });
};

$('#history_survey').click(() => {
    LoadSurvey(SortDate(data.history_survey));
});

// Load demand details in the table on click
let LoadDemand = (history_demand) => {
    currentTab = 'history_demand';
    let table = 
        `
        <table class="table table-striped table-bordered table-hover dt-responsive" width="100%" id="sample_3" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th class="all">Pattern Number</th>
                    <th class="all">Class of Equipment</th>
                    <th class="all">Spare description</th>
                    <th class="min-phone-l">Demand Number</th>
                    <th class="min-tablet">Quantity Demanded</th>
                    <th class="none">Demand Date</th>
                    <th class="none">Remarks</th>
                </tr>
            </thead>
            <tbody>
        `;

    let e = history_demand;
    for (var i = e.length - 1; i >= 0; i--) {
        table += `
            <tr>
                <td>${e[i].pattern_number}</td>
                <td>${e[i].equipment_class}</td>
                <td>${e[i].description}</td>  
                <td>${e[i].demand_number}</td>
                <td>${e[i].quantity}</td>
                <td>${e[i].date}</td>
                <td>${e[i].remarks}</td>
            </tr>`;
    }

    table +=`</tbody></table>`;

    $('#table_head').html('Spares Demanded');
    $('#table').html(table);
    $.ajax({
        url: "/static/assets/pages/scripts/table-datatables-responsive.js",
        dataType: "script",
        success: () => {}
    });
};

$('#history_demand').click(() => {
    LoadDemand(SortDate(data.history_demand));
});

// Load receive details in the table on click
let LoadReceive = (history_receive) => {
    currentTab = 'history_receive';
    let table = 
        `
        <table class="table table-striped table-bordered table-hover dt-responsive" width="100%" id="sample_3" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th class="all">Pattern Number</th>
                    <th class="all">Class of Equipment</th>
                    <th class="all">Spare description</th>
                    <th class="all">Receipt Number</th>
                    <th class="min-phone-l">Quantity Received</th>
                    <th class="none">Receipt Date</th>                    
                    <th class="none">Remarks</th>
                </tr>
            </thead>
            <tbody>
        `;

    let e = history_receive;
    for (var i = e.length - 1; i >= 0; i--) {
        table += `
            <tr>
                <td>${e[i].pattern_number}</td>
                <td>${e[i].equipment_class}</td>
                <td>${e[i].description}</td>  
                <td>${e[i].receipt_number}</td>
                <td>${e[i].quantity}</td>
                <td>${e[i].date}</td>
                <td>${e[i].remarks}</td>
            </tr>`;
    }

    table +=`</tbody></table>`;

    $('#table_head').html('Spares Received');
    $('#table').html(table);
    $.ajax({
        url: "/static/data/js/datatable_history_responsive.js",
        dataType: "script",
        success: () => {}
    });
};

$('#history_receive').click(() => {
    LoadReceive(SortDate(data.history_receive));
});


// Load the issue table by default
$(document).ready(() => {
    setTimeout(() => {
        $('#history_issue').trigger('click');
    }, 1);

    // Daterange selector
    $('#span_date').on('DOMSubtreeModified', () => {
        if ($('#span_date').text() != ''){
            $(`#${currentTab}`).trigger('click');
        }
    });

});
