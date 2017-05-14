/*---------------------------------------
View Select
---------------------------------------*/
var userSheetList,
    publicSheetList,
    fullSheetList,
    sheetID = null,
    btnActive = false;

function getSheetList(requestType) {
    queryType = {"requestType": requestType};
    return $.ajax({
        type: "POST",
        url: '/get-sheets',
        data: JSON.stringify(queryType),
        contentType: 'application/json',
        success: function(result) {
            userSheetList = result['sheets'];
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function postSheetID(id, googleID, sheetName) {
    $("#spinner").show();
    var dataJson = {"sheetID": id, "googleID": googleID, "sheetName": sheetName};
    console.log(dataJson);
    return $.ajax({
        type: "POST",
        url: '/save-sheet',
        data: JSON.stringify(dataJson),
        contentType: 'application/json',
        success: function(result) {
            if(result['status'] === "Success") {
                window.location = "./view-cards";
            };
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function generateSheetList(div, data) {
    var header = "<thead><tr>",
        rows = "<tbody>",
        colHeader,
        colName;

    // Create Header
    for (col in tableMappings[div]["cleanNames"]) {
        colHeader = tableMappings[div]["cleanNames"][col];
        header = header + '<th>' + colHeader + '</th>';
    }
    header = header + '<th class="confirm-head">Options</th></tr></thead>';

    // Create Data Rows
    for (sheet in data) {
        rows = rows + '<tr class="table-row" id="' + data[sheet]['id'] + '">'
        for (key in tableMappings[div]["columns"]) {
            colName = tableMappings[div]["columns"][key];
            rows = rows + '<td>' + data[sheet][colName] + '</td>';
        };

        // Add Column for Accept button
        rows = rows + '<td class="confirm-col">' + '' + '</td>';
        rows = rows + '</tr>';
    };
    rows = rows + "</tbody>";

    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);
};

function selectRow(div, id) {
    $(".confirm-col").empty();
    if (!$("#" + String(id)).hasClass("selected")) {
        var button = '<button type="button" class="btn btn-success btn-sm" id="accept-btn" onclick="confirmSelection(\'' + id + '\')">View</button>'
        $("#" + id + "> .confirm-col").append(button);
    };
};

function confirmSelection(id) {
    event.stopPropagation();
    var sheetName = $('#' + id).children('td').first().text();
    var googleID = getGoogleID(id, userSheetList);
    postSheetID(id, googleID, sheetName);
};

function getGoogleID(id, data) {
    for (row in data) {
        if (Number(data[row]['id']) == Number(id)){
            return data[row]['google_id'];
        };
    };
};

$(document).ready(function(){
    // $('#accept-link').bind('click', false);
    $("#spinner").show();
    // Get Account Structure Data
    $.when(getSheetList('initial view')).done( function() {
        generateSheetList("user-most-viewed", userSheetList);
        $('#user-most-viewed').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        // $('#public-most-viewed').DataTable({
        //     'order': [[ 1, "desc" ]],
        //     'lengthChange': false,
        //     'select': 'single'
        // });
        //
        // $('#full-list').DataTable({
        //     'order': [[ 1, "desc" ]],
        //     'lengthChange': false,
        //     'select': 'single'
        // });

        $(".table-row").on('click', function () {
            var tableID = $(this).parent().parent().attr('id');
            selectRow(tableID, this.id);
        });

        $('#accept-btn').on('click', function () {

        });
    });
});
