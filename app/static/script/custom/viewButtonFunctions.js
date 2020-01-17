// VIEW BUTTON FUNCTIONS
function addViewButton(div) {
    $("#" + div + " .table-row").on('click', function () {
        showViewButton(div, this.id, $(this).attr('data-value'));
    });
}


function showViewButton(div, row_id, sheet_id) {
    $( "#" + div + "-view").remove();
    const cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        var view_button = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
                   + 'id="' + div + '-view"'
                   + 'onclick="viewSheet(' + sheet_id + ', event)">'
                   + '<i class="fa fa-play" aria-hidden="true"></i></button>'

       $(cellID).append(view_button);
    }
}


function viewSheet(id, event) {

    event.stopPropagation();
    $.when(registerSheetView(id)).done( function() {
        window.location = "./flashcards/" + String(id);
    })
}


function registerSheetView(id) {
    $("#spinner").show();
    const dataJson = {"sheetID": id};
    return $.ajax({
        type: "POST",
        url: '/register-sheet-view',
        data: JSON.stringify(dataJson),
        contentType: 'application/json',
        success: function(result) {
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    })
}
