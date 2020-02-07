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
            });
        }
        else {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, viewColumn), "desc" ]],
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
        googleIdIndex = null,
        statusIndex = null;

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
            headerHtml += '<th class="' + getSheetColumnClass(column) + '">' + column + '</th>';
        })
        headerHtml += '<th class="all confirm-head">Options</th></tr>';

        // Data Rows
        sheetIdIndex = tableData['columns'].indexOf("sheetId");
        googleIdIndex = tableData['columns'].indexOf("googleId");
        statusIndex = tableData['columns'].indexOf("Status");
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
    if (tableData != null) {
        addAllButtons(div, tableData, buttonsToAdd, sheetIdIndex, googleIdIndex, statusIndex);
    }

    return viewColumn;
}


function addTableRow(rowData, div, sheetIdIndex, googleIdIndex){
    const sheetId = String(rowData[sheetIdIndex]);
    const googleId = String(rowData[googleIdIndex]);
    const htmlId = div + '-' + sheetId;

    let rowHtml = '<tr class="table-row">'
    const rowCopy = rowData.slice();
    rowCopy.splice(2, rowCopy.length).map(function(dataPoint) {
        rowHtml += '<td>' + dataPoint + '</td>';
    });

    // Add column for buttons
    rowHtml += '<td class="confirm-col" id="opt-' + htmlId + '">' + ' ' + '</td>';
    rowHtml += '</tr>';

    return rowHtml;
}


function addAllButtons(div, tableData, buttonsToAdd, sheetIdIndex, googleIdIndex, statusIndex){

    if (typeof buttonsToAdd !== "undefined") {
        if (buttonsToAdd.includes("viewButton")) {
            addViewButtons(div, tableData['data'], sheetIdIndex);
        };
        if (buttonsToAdd.includes("shareButton")) {
            addShareButtons(div, tableData['data'], sheetIdIndex, googleIdIndex, statusIndex);
        };
        if (buttonsToAdd.includes("reviewButton")) {
            addReviewButtons(div, tableData['data'], sheetIdIndex, googleIdIndex);
        };
        if (buttonsToAdd.includes("approveButton")) {
            addApproveButtons(div, tableData['data'], sheetIdIndex, googleIdIndex);
        };
        if (buttonsToAdd.includes("privateButton")) {
            addPrivateButtons(div, tableData['data'], sheetIdIndex, googleIdIndex, statusIndex);
        };
        if (buttonsToAdd.includes("cancelButton")) {
            addCancelButtons(div, tableData['data'], sheetIdIndex, googleIdIndex, statusIndex);
        };
    }
}
