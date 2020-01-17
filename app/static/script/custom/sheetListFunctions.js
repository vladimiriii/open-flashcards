function getSheetLists(table, additionalButtons) {
    $("#spinner").show();
    $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        data: {"table": table},
        success: function(result) {
            createTables(table, result["data"], additionalButtons)
        },
        error: function(msg){
            console.log(msg);
        }
    });
}


function createTables(table, data, additionalButtons) {
    $.when(generateSheetList(table, data)).done(function(){
        $('#' + table).DataTable({
            'order': [[ 2, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });
        addViewButton(table);

        if (typeof additionalButtons !== "undefined") {
            if (additionalButtons.includes("shareButton")) {
                addShareButton(table);
            }
        }
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
