/*---------------------------------------
View Select
---------------------------------------*/
var userSheetList,
    publicSheetList,
    fullSheetList,
    sharedSheetID = null,
    btnActive = false,
    importComplete = false;

function getSheetList(requestType) {
    $("#spinner").show();
    var queryType = {"requestType": requestType};
    return $.ajax({
        type: "POST",
        url: '/get-sheets',
        data: JSON.stringify(queryType),
        contentType: 'application/json',
        success: function(result) {
            if (requestType == 'initial view') {
                userSheetList = result['user_list'];
                publicSheetList = result['public_list'];
            } else if (requestType == 'full list') {
                fullSheetList = result['sheets'];
            };
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function importSheetInfo(googleSheetID) {
    $("#spinner").show();
    var dataJson = {"sheetID": googleSheetID};
    return $.ajax({
        type: "POST",
        url: '/import-sheet',
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

function postSheetID(id, googleID) {
    $("#spinner").show();
    var dataJson = {"sheetID": id, "googleID": googleID};
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


function openSheetAccess(sheetID) {
    $("#spinner").show();
    var dataJSON = {"sheetID": sheetID};
    return $.ajax({
        type: "POST",
        url: '/open-sheet',
        data: JSON.stringify(dataJSON),
        contentType: 'application/json',
        success: function(result) {
            if (result['status'] == 'sheet shared') {
                $('#share-btn-success-modal').modal('show');
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
    $('#' + div).empty();
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
        rows = rows + '<tr class="table-row" data-value="' + data[sheet]['id'] + '" id="' + div.substring(0, 2) + data[sheet]['id'] + '">'
        for (key in tableMappings[div]["columns"]) {
            colName = tableMappings[div]["columns"][key];
            rows = rows + '<td>' + data[sheet][colName] + '</td>';
        };

        // Add Column for View/Import button
        rows = rows + '<td class="confirm-col" id="' + div.substring(0, 2) + data[sheet]['id'] + '-opt">' + '' + '</td>';
        rows = rows + '</tr>';
    };
    rows = rows + "</tbody>";

    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);
};


function selectRow(div, row_id, sheet_id) {
    $("td.confirm-col").empty();
    var cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        // Users Private List
        if (div == 'user-most-viewed') {
            // View Button
            var view_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                       + 'id="' + div + '-accept"'
                       + 'onclick="confirmSelection(' + sheet_id + ')">'
                       + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

            // Share Button
            var share_button = '<button type="button" class="btn btn-warning btn-sm confirm-col-btn"'
                       + ' id="make-public" onclick="openSheetAccess(' + sheet_id + ')">'
                       + '<span class="glyphicon glyphicon-share" aria-hidden="true"></span></button>'

            // Append Buttons
            $(cellID).append(view_button);
            $(cellID).append(share_button);

        // Public Sheets List
        } else if (div == 'public-most-viewed') {
            // View Button
            var view_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                       + 'id="' + div + '-accept"'
                       + 'onclick="confirmSelection(' + sheet_id + ')">'
                       + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

           // Append Button
           $(cellID).append(view_button);

        // Import Sheet List
        } else if (div == 'full-list') {
            // Import Button
            var import_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                       + 'id="' + div + '-accept"'
                       + 'onclick="importSheet(\'' + sheet_id + '\')">'
                       + '<span class="glyphicon glyphicon-save" aria-hidden="true"></span></button>'

            // Append Button
            $(cellID).append(import_button);
        };
    };
};

function confirmSelection(id) {
    event.stopPropagation();
    var googleID = getGoogleID(id, userSheetList);
    // console.log(id);
    // console.log(googleID);
    postSheetID(id, googleID);
};

function importSheet(id) {
    event.stopPropagation();
    importSheetInfo(id);
};

function getGoogleID(id, data) {
    for (row in data) {
        if (Number(data[row]['id']) == Number(id)){
            return data[row]['google_id'];
        };
    };
};

$(document).ready(function(){

    // Get Account Structure Data
    $.when(getSheetList('initial view')).done( function() {
        generateSheetList("user-most-viewed", userSheetList);
        $('#user-most-viewed').DataTable({
            'order': [[ 2, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        generateSheetList("public-most-viewed", publicSheetList);
        $('#public-most-viewed').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        $("#user-most-viewed .table-row").on('click', function () {
            selectRow("user-most-viewed", this.id, $(this).attr('data-value'));
        });

        $("#public-most-viewed .table-row").on('click', function () {
            selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
        });
    });


    $("#import-sheet").on('click', function() {
        // Only import full list once
        if (!importComplete) {
            $.when(getSheetList('full list')).done( function() {
                generateSheetList("full-list", fullSheetList);
                $('#full-list').DataTable({
                    'order': [[ 1, "desc" ]],
                    'lengthChange': false,
                    'select': 'single'
                });
                importComplete = true;

                $("#full-list .table-row").on('click', function () {
                    selectRow('full-list', this.id, $(this).attr('data-value'));
                });
            });
        };
    });

    $('#share-sheet-success-btn').on('click', function() {
        $('#share-btn-success-modal').modal('hide');

        // Refresh Public Data Table
        $.when(getSheetList('initial view')).done( function() {
            generateSheetList("public-most-viewed", publicSheetList);

            $("#public-most-viewed .table-row").on('click', function () {
                selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
            });
        });

    });

});
