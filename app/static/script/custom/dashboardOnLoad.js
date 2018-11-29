/*---------------------------------------
View Select
---------------------------------------*/
var userSheetList,
    publicSheetList,
    fullSheetList,
    importComplete = false;

$(document).ready(function(){

    // Get Account Structure Data
    $.when(getSheetList('initial view')).done( function() {
        generateSheetList("user-most-viewed", userSheetList);
        $('#user-most-viewed').DataTable({
            'order': [[ 2, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        generateSheetList("public-most-viewed", publicSheetList);
        $('#public-most-viewed').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        $("#user-most-viewed .table-row").on('click', function () {
            selectRow("user-most-viewed", this.id, $(this).attr('data-value'));
        });

        $("#public-most-viewed .table-row").on('click', function () {
            selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
        });
    });


    $("#import-sheet").on('click', function() {
        // Only import full list once
        if (!importComplete) {
            $.when(getSheetList('full list')).done( function() {
                generateSheetList("full-list", fullSheetList);
                $('#full-list').DataTable({
                    'order': [[ 1, "desc" ]],
                    'lengthChange': false,
                    'select': 'single'
                });
                importComplete = true;

                $("#full-list .table-row").on('click', function () {
                    selectRow('full-list', this.id, $(this).attr('data-value'));
                });
            });
        };
    });

    $('#share-sheet-success-btn').on('click', function() {
        $('#share-btn-success-modal').modal('hide');

        // Refresh Public Data Table
        $.when(getSheetList('initial view')).done( function() {
            generateSheetList("public-most-viewed", publicSheetList);

            $("#public-most-viewed .table-row").on('click', function () {
                selectRow("public-most-viewed", this.id, $(this).attr('data-value'));
            });
        });

    });

});
