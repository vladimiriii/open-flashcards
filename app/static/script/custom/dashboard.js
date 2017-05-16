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
            if (result['status'] == 'access needed') {
                $('#share-btn-modal').modal('show');
                sharedSheetID = sheetID;
            } else if (result['status'] == 'sheet shared') {
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

function getAdditionalScope() {
    window.location = "./share-access";
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
        rows = rows + '<tr class="table-row" id="' + data[sheet]['id'] + '">'
        for (key in tableMappings[div]["columns"]) {
            colName = tableMappings[div]["columns"][key];
            rows = rows + '<td>' + data[sheet][colName] + '</td>';
        };

        // Add Column for View/Import button
        rows = rows + '<td class="confirm-col">' + '' + '</td>';
        rows = rows + '</tr>';
    };
    rows = rows + "</tbody>";

    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);
};


function selectRow(div, id, btnFunction, btnText) {
    $("#" + div + " .confirm-col").empty();
    if (!$("#" + String(id)).hasClass("selected")) {
        var button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" id="' + div + '-accept" onclick="' + btnFunction + '(\'' + id + '\')">' + btnText + '</button>'
        $("#" + id + "> .confirm-col").append(button);

        // Additional user table buttons
        if (div == 'user-most-viewed') {
            var button = '<button type="button" class="btn btn-warning btn-sm confirm-col-btn" id="make-public" onclick="openSheetAccess(\'' + id + '\')">Share</button>'
            $("#" + id + "> .confirm-col").append(button);
        };
    };
};

function confirmSelection(id) {
    event.stopPropagation();
    var googleID = getGoogleID(id, userSheetList);
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
            selectRow("user-most-viewed", this.id, "confirmSelection", "View");
        });

        $("#public-most-viewed .table-row").on('click', function () {
            selectRow("public-most-viewed", this.id, "confirmSelection", "View");
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
                    selectRow('full-list', this.id, "importSheet", "Import");
                });
            });
        };
    });

    $('#share-sheet-success-btn').on('click', function() {
        $('#share-btn-success-modal').modal('hide');

        // Refresh Public Data Table
        $.when(getSheetList('initial view')).done( function() {
            generateSheetList("public-most-viewed", publicSheetList);
        });
    });

});
