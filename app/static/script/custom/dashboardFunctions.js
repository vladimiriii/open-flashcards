  /*---------------------------------------
View Select
---------------------------------------*/
function getSheetLists() {
    $("#spinner").show();

    return $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        success: function(result) {
            userSheetList = result['user_list'];
            publicSheetList = result['public_list'];
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function viewSheet(id, googleID) {
    $("#spinner").show();
    var dataJson = {"sheetID": id, "googleID": googleID};
    return $.ajax({
        type: "POST",
        url: '/view-sheet',
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

function checkScopes(scope, callback) {
    return $.ajax({
        type: "GET",
        url: '/check-drive-scopes',
        contentType: 'application/json',
        success: function(result) {
          scope_status = result[scope];
          callback(scope_status)
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function getImportList() {
    $("#spinner").show();

    return $.ajax({
        type: "GET",
        url: '/get-import-options',
        success: function(result) {
            fullSheetList = result['sheets'];
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

function openSheetAccess(sheetID) {
    $("#spinner").show();
    var dataJSON = {"sheetID": sheetID};
    return $.ajax({
        type: "POST",
        url: '/make-sheet-public',
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
                       + 'onclick="confirmSelection(' + sheet_id + ', event)">'
                       + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

            // Share Button
            var share_button = '<button type="button" class="btn btn-warning btn-sm confirm-col-btn"'
                       + ' id="make-public" onclick="openSheetAccess(' + sheet_id + ', event)">'
                       + '<span class="glyphicon glyphicon-share" aria-hidden="true"></span></button>'

            // Append Buttons
            $(cellID).append(view_button);
            $(cellID).append(share_button);

        // Public Sheets List
        } else if (div == 'public-most-viewed') {
            // View Button
            var view_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                       + 'id="' + div + '-accept"'
                       + 'onclick="confirmSelection(' + sheet_id + ', event)">'
                       + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

           // Append Button
           $(cellID).append(view_button);

        // Import Sheet List
        } else if (div == 'full-list') {
            // Import Button
            var import_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                       + 'id="' + div + '-accept"'
                       + 'onclick="importSheet(\'' + sheet_id + '\', event)">'
                       + '<span class="glyphicon glyphicon-save" aria-hidden="true"></span></button>'

            // Append Button
            $(cellID).append(import_button);
        };
    };
};

function confirmSelection(id, event) {
    event.stopPropagation();
    var googleID = getGoogleID(id, userSheetList);
    viewSheet(id, googleID);
};

function generateImportButton(driveAccessFlag) {

    if (driveAccessFlag == 'True') {
      importButton = `<div class="image-btn">
          <a id="import-sheet" href="#full-list-modal" data-toggle="modal"><span class="div-link"></span></a>
          <img class="image-btn-link" src="./static/img/import.png">
          <span class="image-btn-text">Import Cards</span>
      </div>`
    } else {
      importButton = `<div class="image-btn">
          <a id="import-sheet" href="./add-drive-read-scope" data-toggle="modal"><span class="div-link"></span></a>
          <img class="image-btn-link" src="./static/img/import.png">
          <span class="image-btn-text">Allow Imports</span>
      </div>`
    }

    $('#import-btn').append(importButton);
}

function importSheet(id, event) {
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
