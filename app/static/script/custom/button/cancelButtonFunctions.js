// SHARE BUTTON FUNCTIONS
function addCancelButtons(div, tableData, indices) {
    for (rowIndex in tableData) {
        const status = tableData[rowIndex][indices['status']];
        const isOwner = tableData[rowIndex][indices['isOwner']];
        if (status == 'Review Requested' & isOwner) {
            const sheetId = String(tableData[rowIndex][indices['sheetId']]);
            const googleId = String(tableData[rowIndex][indices['googleId']]);
            buildCancelButton(div, sheetId, googleId);
        }
    }
}


function buildCancelButton(div, sheetId, googleId) {
    const cellID = "#opt-" + div + '-' + sheetId;
    const btn = '<button type="button" class="btn btn-outline-danger btn-sm confirm-col-btn" '
           + 'onclick="cancelReviewRequest(\'' + googleId + '\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Cancel request to make public">'
           + '<i class="fa fa-undo" aria-hidden="true"></i></button>'
   $(cellID).append(btn);
}


function cancelReviewRequest(googleId) {
    event.stopPropagation();
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-sheet-status',
        data: JSON.stringify({"googleId": googleId, "event": "Cancel Request"}),
        contentType: 'application/json',
        success: function(result) {
            $("#spinner").hide();
            showResultModal(result['status']);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}
