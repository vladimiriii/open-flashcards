// SHARE BUTTON FUNCTIONS
function addPrivateButtons(div, tableData, indices) {
    for (rowIndex in tableData) {
        const status = tableData[rowIndex][indices['status']];
        const isOwner = tableData[rowIndex][indices['isOwner']];
        if (status == 'Public' & isOwner) {
            const sheetId = String(tableData[rowIndex][indices['sheetId']]);
            const googleId = String(tableData[rowIndex][indices['googleId']]);
            buildPrivateButton(div, sheetId, googleId);
        }
    }
}


function buildPrivateButton(div, sheetId, googleId) {
    const cellID = "#opt-" + div + '-' + sheetId;
    const btn = '<button type="button" class="btn btn-outline-primary btn-sm confirm-col-btn" '
           + 'onclick="makePrivateRequest(\'' + googleId + '\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Make this sheet private again">'
           + '<i class="fa fa-eye-slash" aria-hidden="true"></i></button>'
   $(cellID).append(btn);
}


function makePrivateRequest(googleId) {
    event.stopPropagation();
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-sheet-status',
        data: JSON.stringify({"googleId": googleId, "event": "Make Private"}),
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
