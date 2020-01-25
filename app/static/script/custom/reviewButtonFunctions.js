// REVIEW BUTTON FUNCTIONS
function addReviewButton(div) {
    $("#" + div + " .table-row").on('click', function () {
        showReviewButton(div, this.id, $(this).attr('data-sheet-id'), $(this).attr('data-google-id'));
    });
}


function showReviewButton(div, rowId, sheetId, googleId) {
    $( "#btn-" + div + "-review").remove();
    const cellId = "#opt-" + div + '-' + sheetId;
    if (!$("#" + String(rowId)).hasClass("selected")) {
        const reviewButton = '<button type="button" class="btn btn-outline-danger btn-sm confirm-col-btn" '
                   + 'id="btn-' + div + '-review"'
                   + 'onclick="reviewSheet(\'' + googleId + '\')">'
                   + '<i class="fa fa-eye" aria-hidden="true"></i></button>'

       $(cellId).append(reviewButton);
    }
}


function reviewSheet(googleId) {
    event.stopPropagation();
    const url = "https://docs.google.com/spreadsheets/d/" + googleId;
    const win = window.open(url, '_blank');
    win.focus();
}