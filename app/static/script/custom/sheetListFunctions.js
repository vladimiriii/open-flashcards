function getSheetLists(table, additionalButtons) {
    $("#spinner").show();
    $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        data: {"table": table},
        success: function(result) {
            createTables(table, result, additionalButtons)
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


function generateSheetList(div, tableData) {
    $('#' + div).empty();
    let header = "<thead><tr>",
        rows = "<tbody>";

    // Create Header
    tableData['columns'].splice(2, tableData['columns'].length).map( function(column) {
        header = header + '<th>' + column + '</th>';
    })
    header = header + '<th class="confirm-head">Options</th></tr></thead>';

    // Create Data Rows
    const sheetIdColumn = tableData['columns'].indexOf("sheetId");
    tableData['data'].map( function(rowData) {
        rows = rows + '<tr class="table-row" data-value="' + rowData[sheetIdColumn] + '" id="' + div.substring(0, 2) + rowData[sheetIdColumn] + '">'
        rowData.splice(2, rowData.length).map(function(dataPoint) {
            rows = rows + '<td>' + dataPoint + '</td>';
        });

        // Add column for buttons
        rows = rows + '<td class="confirm-col" id="' + div.substring(0, 2) + rowData[sheetIdColumn] + '-opt">' + '' + '</td>';
        rows = rows + '</tr>';
    });
    rows = rows + "</tbody>";

    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);
}
