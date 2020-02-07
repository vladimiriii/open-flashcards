// REVIEW BUTTON FUNCTIONS
function addReviewButtons(div, tableData, sheetIdIndex, googleIdIndex) {
    for (rowIndex in tableData) {
        const sheetId = String(tableData[rowIndex][sheetIdIndex]);
        const googleId = String(tableData[rowIndex][googleIdIndex]);
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
               + 'data-toggle="modal" data-target="#approveModal">'
               + '<i class="fa fa-check-circle-o" aria-hidden="true"></i></button>'

   $(cellId).append(approveButton);
}
