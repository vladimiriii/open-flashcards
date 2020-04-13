// SHARE BUTTON FUNCTIONS
function addShareButtons(div, tableData, indices) {
    for (rowIndex in tableData) {
        const status = tableData[rowIndex][indices['status']];
        const isOwner = tableData[rowIndex][indices['isOwner']];
        // console.log(status + " - " + isOwner);
        if (status == 'Private' & isOwner) {
            const sheetId = String(tableData[rowIndex][indices['sheetId']]);
            const googleId = String(tableData[rowIndex][indices['googleId']]);
            buildShareButton(div, sheetId, googleId);
        }
    }
}


function buildShareButton(div, sheetId, googleId) {
    const cellID = "#opt-" + div + '-' + sheetId;
    const shareButton = '<button type="button" class="btn btn-outline-warning btn-sm confirm-col-btn" '
           + 'onclick="makeSheetPublic(\'' + googleId + '\', event)"'
           + 'data-toggle="tooltip" data-placement="top" title="Share this sheet">'
           + '<i class="fa fa-share-alt" aria-hidden="true"></i></button>'
   $(cellID).append(shareButton);
}


function makeSheetPublic(id, event) {
    event.stopPropagation();
    $.when(generateShareModal(id)).done(function() {
        $('#shareModal').modal('show');
    })

}


function generateShareModal(id) {
    $("#service-account").empty();
    $("#sheet-link").empty();
    const handle = "guest-user";
    const domain = "flashcard-app-166512.iam.gserviceaccount.com";
    $("#service-account").append(handle + "@" + domain);

    // Copy Icon
    $("#copy-icon").on("click", function() {
        const value = $("#service-account").parent().children("span").html();
        navigator.clipboard.writeText(value);
    });

    // Generate sheet link
    generateSheetLink(id);

    // Submit Button
    $('#modalSubmit:not(.bound)').addClass('bound').click(function() {
        submitShareRequest();
    });
}


function generateSheetLink(googleId) {
    const base_url = "https://docs.google.com/spreadsheets/d/";
    const url = base_url + googleId;
    const html = 'Link to Spreadsheet: <a target="_blank" href=' + url + '>' + url + '</a>';
    $("#sheet-link").append(html);
    $("#modalSubmit").val(googleId);
}


function submitShareRequest() {
    const googleId = $("#modalSubmit").val();
    console.log(googleId);
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-sheet-status',
        data: JSON.stringify({"googleId": googleId, "event": "Request Public"}),
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
