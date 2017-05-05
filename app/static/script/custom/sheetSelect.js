/*---------------------------------------
View Select
---------------------------------------*/
var sheetList,
    sheetID = null,
    btnActive = false;

function getSheetList() {
    $("#spinner").show();
    return $.ajax({
        type: "GET",
        url: '/save-sheet',
        contentType: 'application/json',
        success: function(result) {
            sheetList = result['sheets'];
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

function postSheetID() {
    var dataJson = {"sheet_id": sheetID};
    return $.ajax({
        type: "POST",
        url: '/save-sheet',
        data: JSON.stringify(dataJson),
        contentType: 'application/json',
        success: function() {
            console.log("Success!")
        },
        error: function(msg){
            console.log(msg);
        }
    });
};

function generateSheetList() {
    var rows = "<tbody>";

    for (sheet in sheetList) {
        rows = rows + '<tr class="table-row" id="' +
                sheetList[sheet]['id'] + '"><td>' +
                sheetList[sheet]['name'] + '</td><td>' +
                sheetList[sheet]['modified'] + '</td></tr>';
    };

    rows = rows + "</tbody>";
    $('#sheet_list').append(rows)
};

function selectRow(id) {
    if (sheetID == null) {
        sheetID = id;
        $('#accept-btn').removeClass('disabled');
        $('#accept-link').unbind('click', false);
        btnActive = true;
    } else if (sheetID != null && id != sheetID) {
        sheetID = id;
    } else if (id == sheetID) {
        sheetID = null;
        btnActive = false;
        $('#accept-btn').addClass('disabled');
        $('#accept-link').bind('click', false);
    };
    postSheetID();
};

$(document).ready(function(){
    $('#accept-link').bind('click', false);

    // Get Account Structure Data
    $.when(getSheetList()).done( function() {
        generateSheetList();
        $('#sheet_list').DataTable({
            'order': [[ 1, "desc" ]],
            'lengthChange': false,
            'select': 'single'
        });

        $(".table-row").on('click', function () {
            selectRow(this.id);
        });
    });

    $('#accept-btn').on('click', function () {
        if (btnActive) {
            sheetID = null;
            btnActive = false;
        };
    });

});
