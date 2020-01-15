function getSheetLists(table) {
    $("#spinner").show();
    $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        data: {"table": table},
        success: function(result) {
            createTables(table, result["data"])
        },
        error: function(msg){
            console.log(msg);
        }
    });
}


function createTables(table, data) {
    $.when(generateSheetList(table, data)).done(function(){
        $('#' + table).DataTable({
            'order': [[ 2, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });
        addViewButton(table);
        $("#spinner").hide();
    });
}


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
}


function addViewButton(div) {
    $("#" + div + " .table-row").on('click', function () {
        showViewButton(div, this.id, $(this).attr('data-value'));
    });
}


function showViewButton(div, row_id, sheet_id) {
    $( "#" + div + "-accept").remove();
    var cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        var view_button = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
                   + 'id="' + div + '-accept"'
                   + 'onclick="confirmSelection(' + sheet_id + ', event)">'
                   + '<i class="fa fa-play-circle" aria-hidden="true"></i></button>'

       $(cellID).append(view_button);
    }
}


function addShareButton(div) {
    $("#" + div + " .table-row").on('click', function () {
            showShareButton(div, this.id, $(this).attr('data-value'));
    });
}


function showShareButton(div, row_id, sheet_id) {
    $( "#" + div + "-share").remove();
    var cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        var view_button = '<button type="button" class="btn btn-warning btn-sm confirm-col-btn" '
                   + 'id="' + div + '-accept"'
                   + 'onclick="confirmSelection(' + sheet_id + ', event)">'
                   + '<span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>'

       $(cellID).append(view_button);
    }
}


function confirmSelection(id, event) {

    event.stopPropagation();
    $.when(registerSheetView(id)).done( function() {
        window.location = "./flashcards/" + String(id);
    })
}


function registerSheetView(id) {
    $("#spinner").show();
    const dataJson = {"sheetID": id};
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
    })
}
