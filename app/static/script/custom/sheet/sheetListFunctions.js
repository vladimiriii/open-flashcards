async function createTable(table, buttonsToAdd) {
    const data = await getSheetLists(table);

    const infoColumns = 3
    $.when(generateSheetList(table, data, buttonsToAdd, infoColumns)).done(function(viewColumn){
        if (viewColumn !== -infoColumns) {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, viewColumn - infoColumns), "desc" ]],
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


function getSheetLists(table) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: '/get-sheet-lists',
            data: {"table": table},
            success: (response) => {
                resolve(response);
            },
            error: (response) => {
                reject(response);
            }
        })
    })
}


function generateSheetList(div, tableData, buttonsToAdd, infoColumns) {
    $('#' + div).empty();
    let viewColumn = -infoColumns,
        headerHtml = "",
        rowHtml = "",
        indices = null;

    // Generate Table HTML
    if (tableData == null) {
        headerHtml += '<tr><th>Results</th></tr>';
        rowHtml += '<tr class="table-row"><td>No results found.</td></tr>';
    } else {
        // Header
        headerHtml += '<tr>'
        viewColumn = tableData['columns'].indexOf('Views');
        const columnList = tableData['columns'].slice();
        columnList.splice(infoColumns, tableData['columns'].length).map( function(column) {
            headerHtml += '<th class="' + getSheetColumnClass(column) + '">' + column + '</th>';
        })
        headerHtml += '<th class="all confirm-head">Options</th></tr>';

        // Data Rows
        indices = getColumnIndices(tableData);
        for (rowIndex in tableData['data']) {
            rowHtml += addTableRow(tableData['data'][rowIndex], div, indices['sheetId'], infoColumns);
        }
    }
    const rows = "<tbody>" + rowHtml + "</tbody>";
    const header = "<thead>" + headerHtml + "</thead>";


    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);

    // Append Buttons
    if (tableData != null) {
        addAllButtons(div, tableData, buttonsToAdd, indices);
    }

    return viewColumn;
}


function addTableRow(rowData, div, sheetIdIndex, infoColumns){
    const sheetId = String(rowData[sheetIdIndex]);
    const htmlId = div + '-' + sheetId;

    let rowHtml = '<tr class="table-row">'
    const rowCopy = rowData.slice();
    rowCopy.splice(infoColumns, rowCopy.length).map(function(dataPoint) {
        rowHtml += '<td>' + dataPoint + '</td>';
    });

    // Add column for buttons
    rowHtml += '<td class="confirm-col" id="opt-' + htmlId + '">' + ' ' + '</td>';
    rowHtml += '</tr>';

    return rowHtml;
}


async function addAllButtons(div, tableData, buttonsToAdd, indices){
    const userRole = await getUserRole();

    if (typeof buttonsToAdd !== "undefined") {
        if (buttonsToAdd.includes("viewButton")) {
            addViewButtons(div, tableData['data'], indices);
        };
        if (buttonsToAdd.includes("shareButton")) {
            addShareButtons(div, tableData['data'], indices);
        };
        if (buttonsToAdd.includes("reviewButton")) {
            addReviewButtons(div, tableData['data'], indices);
        };
        if (buttonsToAdd.includes("approveButton")) {
            addApproveButtons(div, tableData['data'], indices);
        };
        if (buttonsToAdd.includes("privateButton")) {
            addPrivateButtons(div, tableData['data'], indices);
        };
        if (buttonsToAdd.includes("cancelButton")) {
            addCancelButtons(div, tableData['data'], indices);
        };
    }
}
