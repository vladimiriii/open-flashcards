// SHARE BUTTON FUNCTIONS
function addPrivateButtons(div, tableData, sheetIdIndex, googleIdIndex, statusIndex) {
    for (rowIndex in tableData) {
        const status = tableData[rowIndex][statusIndex]
        if (status == 'Public') {
            const sheetId = String(tableData[rowIndex][sheetIdIndex]);
            const googleId = String(tableData[rowIndex][googleIdIndex]);
            buildPrivateButton(div, sheetId, googleId);
        }
    }
}


function buildPrivateButton(div, sheetId, googleId) {
    const cellID = "#opt-" + div + '-' + sheetId;
    const btn = '<button type="button" class="btn btn-outline-primary btn-sm confirm-col-btn" '
           + 'onclick="makePrivateRequest(\'' + googleId + '\')">'
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
