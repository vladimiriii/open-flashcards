/*-----------------------------------
Global Variables
-----------------------------------*/
var publicSheetList,
    userSheetList,
    scope_status,
    importComplete = false;

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    // Get Account Structure Data
    $.when(getSheetLists(false)).done( function() {

        generateSheetList("public-cards", publicSheetList);
        $('#public-cards').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        $("#public-cards .table-row").on('click', function () {
            showViewButton("public-cards", this.id, $(this).attr('data-value'));
        });
    });

//    $('#share-sheet-success-btn').on('click', function() {
//        $('#share-btn-success-modal').modal('hide');
//
//        // Refresh Public Data Table
//        $.when(getSheetLists('initial view')).done( function() {
//            generateSheetList("public-cards", publicSheetList);
//
//            $("#public-cards .table-row").on('click', function () {
//                selectRow("public-cards", this.id, $(this).attr('data-value'));
//            });
//        });
//    });
});
