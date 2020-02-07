// VIEW BUTTON FUNCTIONS
function addViewButtons(div, tableData, sheetIdIndex) {
    for (rowIndex in tableData) {
        const sheetId = String(tableData[rowIndex][sheetIdIndex]);
        buildViewButton(div, sheetId);
    }
}


function buildViewButton(div, sheetId) {
    const cellID = "#opt-" + div + '-' + sheetId;
    const viewButton = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
               + 'onclick="viewSheet(' + sheetId + ', event)"'
               + 'data-toggle="tooltip" data-placement="top" title="View the flashcards">'
               + '<i class="fa fa-play" aria-hidden="true"></i></button>'
   // console.log(viewButton);
   $(cellID).append(viewButton);
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
