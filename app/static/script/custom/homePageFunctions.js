function getSheetLists() {
    $("#spinner").show();

    return $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        success: function(result) {
            console.log(result);
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


function registerSheetView(id, googleID) {
    $("#spinner").show();
    var dataJson = {"sheetID": id, "googleID": googleID};
    return $.ajax({
        type: "POST",
        url: '/register-sheet-view',
        data: JSON.stringify(dataJson),
        contentType: 'application/json',
        success: function(result) {
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
    for (col in tableMappings["cleanNames"]) {
        colHeader = tableMappings["cleanNames"][col];
        header = header + '<th>' + colHeader + '</th>';
    }
    header = header + '<th class="confirm-head">Options</th></tr></thead>';

    // Create Data Rows
    for (sheet in data) {
        rows = rows + '<tr class="table-row" data-value="' + data[sheet]['id'] + '" id="' + div.substring(0, 2) + data[sheet]['id'] + '">'
        for (key in tableMappings["columns"]) {
            colName = tableMappings["columns"][key];
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


function showViewButton(div, row_id, sheet_id) {
    $( "#" + div + "-accept").remove();
    var cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        var view_button = '<button type="button" class="btn btn-success btn-sm confirm-col-btn" '
                   + 'id="' + div + '-accept"'
                   + 'onclick="confirmSelection(' + sheet_id + ', event)">'
                   + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

       $(cellID).append(view_button);
    };
};


function confirmSelection(id, event) {

    event.stopPropagation();
    var googleID = getGoogleID(id, publicSheetList);

    // Register the click and redirect
    $.when(registerSheetView(id, googleID)).done( function() {
        window.location = "./flashcards/" + String(id);
    })
}


function getGoogleID(id, data) {
    for (row in data) {
        if (Number(data[row]['id']) == Number(id)){
            return data[row]['google_id'];
        };
    };
};
