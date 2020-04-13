// REVIEW BUTTON FUNCTIONS
function addReviewButtons(div, tableData, indices) {
    for (rowIndex in tableData) {
        const sheetId = String(tableData[rowIndex][indices['sheetId']]);
        const googleId = String(tableData[rowIndex][indices['googleId']]);
        buildReviewButton(div, sheetId, googleId);
    }
}


function buildReviewButton(div, sheetId, googleId) {
    const cellId = "#opt-" + div + '-' + sheetId;
    const reviewButton = '<button type="button" class="btn btn-outline-danger btn-sm confirm-col-btn" '
               + 'onclick="reviewSheet(\'' + googleId + '\')"'
               + 'data-toggle="tooltip" data-placement="top" title="View the sheet">'
               + '<i class="fa fa-eye" aria-hidden="true"></i></button>'

   $(cellId).append(reviewButton);
}


function reviewSheet(googleId) {
    event.stopPropagation();
    const url = "https://docs.google.com/spreadsheets/d/" + googleId;
    const win = window.open(url, '_blank');
    win.focus();
}


// APPROVE BUTTON
function addApproveButtons(div, tableData, sheetIdIndex, googleIdIndex) {
    for (rowIndex in tableData) {
        const sheetId = String(tableData[rowIndex][sheetIdIndex]);
        const googleId = String(tableData[rowIndex][googleIdIndex]);
        buildApproveButton(div, sheetId, googleId);
    }
}


function buildApproveButton(div, sheetId, googleId) {
    const cellId = "#opt-" + div + '-' + sheetId;
    const approveButton = '<button type="button" class="btn btn-outline-warning btn-sm confirm-col-btn" '
               + 'onclick="generateApproveModal(\'' + googleId + '\')"'
               + 'data-toggle="tooltip" data-placement="top" title="Approve or deny this request">'
               + '<i class="fa fa-check-circle-o" aria-hidden="true"></i></button>'

   $(cellId).append(approveButton);
}

function generateApproveModal(id) {
    event.stopPropagation();
    $.when(generateApproveModalButtons(id)).done(function() {
        $('#approveModal').modal('show');
    })

}

function generateApproveModalButtons(id) {
    $('#approveBtn:not(.bound)').addClass('bound').click(function() {
        requestResponse(id, 'Approve Sheet');
    });
    $('#denyBtn:not(.bound)').addClass('bound').click(function() {
        requestResponse(id, "Cancel Request");
    });
}


function requestResponse(googleId, response) {
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-sheet-status',
        data: JSON.stringify({"googleId": googleId, "event": response}),
        contentType: 'application/json',
        success: function(result) {
            $("#spinner").hide();
            window.location.reload();
        },
        error: function(msg){
            console.log(msg);
        }
    })
}
