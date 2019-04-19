/*-----------------------------------
Global Variables
-----------------------------------*/
var publicSheetList,
    fullSheetList,
    scope_status,
    importComplete = false;

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    // Get Account Structure Data
    $.when(getSheetLists()).done( function() {

        generateSheetList("public-most-viewed", publicSheetList);
        $('#public-most-viewed').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        $("#public-most-viewed .table-row").on('click', function () {
            selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
        });
    });

    // Check scopes to see if import option is available and generate button
    checkScopes('read_scope_present', generateImportButton);

    $('#share-sheet-success-btn').on('click', function() {
        $('#share-btn-success-modal').modal('hide');

        // Refresh Public Data Table
        $.when(getSheetLists('initial view')).done( function() {
            generateSheetList("public-most-viewed", publicSheetList);

            $("#public-most-viewed .table-row").on('click', function () {
                selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
            });
        });
    });
});
