// VIEW BUTTON FUNCTIONS
function addViewButton(div) {
    $("#" + div + " .table-row").on('click', function () {
        showViewButton(div, this.id, $(this).attr('data-sheet-id'));
    });
}


function showViewButton(div, rowId, sheetId) {
    $( "#" + div + "-view").remove();
    const cellID = "#opt-" + div + '-' + sheetId;
    if (!$("#" + rowId).hasClass("selected")) {
        const viewButton = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
                   + 'id="' + div + '-view"'
                   + 'onclick="viewSheet(' + sheetId + ', event)">'
                   + '<i class="fa fa-play" aria-hidden="true"></i></button>'

       $(cellID).append(viewButton);
    }
}


function viewSheet(id, event) {

    event.stopPropagation();
    $.when(registerSheetView(id)).done( function() {
        window.location = "./flashcards/" + id;
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
