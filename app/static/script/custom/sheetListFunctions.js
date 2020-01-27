function getSheetLists(table, buttonsToAdd) {
    $("#spinner").show();
    $.ajax({
        type: "GET",
        url: '/get-sheet-lists',
        data: {"table": table},
        success: function(result) {
            createTables(table, result, buttonsToAdd)
        },
        error: function(msg){
            console.log(msg);
        }
    });
}


function createTables(table, data, buttonsToAdd) {
    $.when(generateSheetList(table, data, buttonsToAdd)).done(function(viewColumn){
        if (viewColumn !== -2) {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, viewColumn - 2), "desc" ]],
                'lengthChange': false,
                'select': false
            });
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


function generateSheetList(div, tableData, buttonsToAdd) {
    $('#' + div).empty();
    let viewColumn = -2,
        headerHtml = "",
        rowHtml = "",
        sheetIdIndex = null,
        googleIdIndex = null;

    // Generate Table HTML
    if (tableData == null) {
        headerHtml += '<tr><th>Results</th></tr>';
        rowHtml += '<tr class="table-row"><td>No results found.</td></tr>';
    } else {
        // Header
        headerHtml += '<tr>'
        viewColumn = tableData['columns'].indexOf('Views');
        const columnList = tableData['columns'].slice();
        columnList.splice(2, tableData['columns'].length).map( function(column) {
            headerHtml += '<th>' + column + '</th>';
        })
        headerHtml += '<th class="confirm-head">Options</th></tr>';

        // Data Rows
        sheetIdIndex = tableData['columns'].indexOf("sheetId");
        googleIdIndex = tableData['columns'].indexOf("googleId");
        for (rowIndex in tableData['data']) {
            rowHtml += addTableRow(tableData['data'][rowIndex], div, sheetIdIndex, googleIdIndex);
        }
    }
    const rows = "<tbody>" + rowHtml + "</tbody>";
    const header = "<thead>" + headerHtml + "</thead>";


    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);

    // Append Buttons
    addAllButtons(div, tableData, buttonsToAdd, sheetIdIndex, googleIdIndex);

    return viewColumn;
}


function addTableRow(rowData, div, sheetIdIndex, googleIdIndex){
    const sheetId = String(rowData[sheetIdIndex]);
    const googleId = String(rowData[googleIdIndex]);
    const htmlId = div + '-' + sheetId;

    let rowHtml = '<tr class="table-row">'
    rowData.splice(2, rowData.length).map(function(dataPoint) {
        rowHtml += '<td>' + dataPoint + '</td>';
    });

    // Add column for buttons
    rowHtml += '<td class="confirm-col" id="opt-' + htmlId + '">' + ' ' + '</td>';
    rowHtml += '</tr>';

    return rowHtml;
}


function addAllButtons(div, tableData, buttonsToAdd, sheetIdIndex, googleIdIndex){

    if (typeof buttonsToAdd !== "undefined") {
        if (buttonsToAdd.includes("viewButton")) {
            addViewButtons(div, tableData['data'], sheetIdIndex);
        };
        if (buttonsToAdd.includes("shareButton")) {
            addShareButtons(div, tableData['data'], sheetIdIndex, googleIdIndex);
        };
        if (buttonsToAdd.includes("reviewButton")) {
            addReviewButtons(div, tableData['data'], sheetIdIndex, googleIdIndex);
        };
        if (buttonsToAdd.includes("approveButton")) {
            addApproveButtons(div, tableData['data'], sheetIdIndex, googleIdIndex);
        };
    }
}
