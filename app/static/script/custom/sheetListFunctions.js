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
    $.when(generateSheetList(table, data)).done(function(viewColumn){
        console.log(viewColumn);
        if (viewColumn !== -2) {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, viewColumn), "desc" ]],
                'lengthChange': false,
                'select': 'single'
            });

            addViewButton(table);

            if (typeof additionalButtons !== "undefined") {
                if (additionalButtons.includes("shareButton")) {
                    addShareButton(table);
                }
            }
        }
        else {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, viewColumn), "desc" ]],
                'select': false,
                'lengthChange': false,
                'searching': false,
                'ordering': false,
                'paging': false,
                'info': false

            });
        }
        $("#spinner").hide();
    });
}


function generateSheetList(div, tableData) {
    $('#' + div).empty();
    let header = "<thead>",
        rows = "<tbody>",
        viewColumn = -2;

    // Generate Table HTML
    if (tableData == null) {
        header += '<tr><th>Results</th></tr>';
        rows += '<tr class="table-row"><td>No results found.</td></tr>';
    } else {
        // Header
        header += '<tr>'
        viewColumn = tableData['columns'].indexOf('Views');
        tableData['columns'].splice(2, tableData['columns'].length).map( function(column) {
            header += '<th>' + column + '</th>';
        })
        header += '<th class="confirm-head">Options</th></tr>';

        // Data Rows
        tableData['data'].map( function(rowData) {
            const sheetId = String(rowData[tableData['columns'].indexOf("sheetId")]);
            const googleId = String(rowData[tableData['columns'].indexOf("googleId")]);
            const htmlId = div + '-' + sheetId;
            rows += '<tr class="table-row" id="row-' + htmlId + '" + data-sheet-id="' + sheetId + '" data-google-id="' + googleId + '">'
            rowData.splice(2, rowData.length).map(function(dataPoint) {
                rows += '<td>' + dataPoint + '</td>';
            });

            // Add column for buttons
            rows += '<td class="confirm-col" id="opt-' + htmlId + '">' + ' ' + '</td>';
            rows += '</tr>';
        });
    }
    header += "</thead>";
    rows += "</tbody>";

    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);

    return viewColumn;
}
