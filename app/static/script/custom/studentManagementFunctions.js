function getStudentListData(table, buttonsToAdd) {
    $("#spinner").show();
    $.ajax({
        type: "GET",
        url: '/get-student-list',
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
    $.when(generateStudentListRows(table, data, buttonsToAdd)).done(function(userColumn){
        if (userColumn !== -1) {
            $('#' + table).DataTable({
                'order': [[ Math.max(0, userColumn), "asc" ]],
                'lengthChange': false,
            });
        }
        else {
            $('#' + table).DataTable({
                "columnDefs": [
                    { "width": "30px", "targets": 1 },
                    { "width": "200px", "targets": 6 }
                 ],
                'order': [[ Math.max(0, userColumn), "asc" ]],
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


function generateStudentListRows(div, tableData, buttonsToAdd) {
    $('#' + div).empty();
    let headerHtml = "",
        rowHtml = "",
        userIdIndex = null;
        roleIndex = null;

    // Generate Table HTML
    if (tableData == null) {
        headerHtml += '<tr><th>Results</th></tr>';
        rowHtml += '<tr class="table-row"><td>No results found.</td></tr>';
    } else {
        // Header
        headerHtml += '<tr>'
        const columnList = tableData['columns'].slice()
        columnList.map(function(column) {
            headerHtml += '<th class="' + getStudentColumnClass(column) + '">' + column + '</th>';
        })
        headerHtml += '<th class="all confirm-head">Options</th></tr>';

        // Data Rows
        userIdIndex = tableData['columns'].indexOf('User ID');
        roleIndex = tableData['columns'].indexOf('Role');
        for (rowIndex in tableData['data']) {
            rowHtml += addTableRow(tableData['data'][rowIndex], div, userIdIndex);
        }
    }
    const rows = "<tbody>" + rowHtml + "</tbody>";
    const header = "<thead>" + headerHtml + "</thead>";


    // Append elements to the Table
    $('#' + div).append(header);
    $('#' + div).append(rows);

    // Append Buttons
    if (tableData != null) {
        addStudentManagementButtons(div, tableData, buttonsToAdd, userIdIndex, roleIndex);
    }

    return userIdIndex;
}


function addTableRow(rowData, div, userIdIndex){
    const userId = String(rowData[userIdIndex]);
    const htmlId = div + '-' + userId;

    let rowHtml = '<tr class="table-row">'
    rowData.map(function(dataPoint) {
        rowHtml += '<td>' + dataPoint + '</td>';
    });

    // Add column for buttons
    rowHtml += '<td class="confirm-col" id="opt-' + htmlId + '">' + ' ' + '</td>';
    rowHtml += '</tr>';

    return rowHtml;
}


function addStudentManagementButtons(div, tableData, buttonsToAdd, userIdIndex, roleIndex){

    // if (typeof buttonsToAdd !== "undefined") {
    //     if (buttonsToAdd.includes("graduateUpgradeButton")) {
    //         addGraduateUpgradeButtons(div, tableData['data'], userIdIndex, roleIndex);
    //     };
    //     if (buttonsToAdd.includes("teacherUpgradeButton")) {
    //         addTeacherUpgradeButtons(div, tableData['data'], userIdIndex, roleIndex);
    //     };
    //     if (buttonsToAdd.includes("cancelPackageButton")) {
    //         addCancelPackageButtons(div, tableData['data'], userIdIndex, roleIndex);
    //     };
    //     if (buttonsToAdd.includes("blockButton")) {
    //         addBlockButtons(div, tableData['data'], userIdIndex, roleIndex);
    //     };
    //     if (buttonsToAdd.includes("unblockButton")) {
    //         addUnblockButtons(div, tableData['data'], userIdIndex, roleIndex);
    //     };
    // }
}
