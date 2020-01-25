// SHARE BUTTON FUNCTIONS
function addShareButton(div) {
    $("#" + div + " .table-row").on('click', function () {
        showShareButton(div, this.id, $(this).attr('data-sheet-id'), $(this).attr('data-google-id'));
    });
}

// SHARE BUTTON FUNCTIONS
function showShareButton(div, rowId, sheetId, googleId) {
    $( "#" + div + "-share").remove();
    const cellID = "#opt-" + div + '-' + sheetId;
    if (!$("#" + String(rowId)).hasClass("selected")) {
        const shareButton = '<button type="button" class="btn btn-outline-warning btn-sm confirm-col-btn" '
                   + 'id="' + div + '-share"'
                   + 'onclick="makeSheetPublic(\'' + googleId + '\', event)">'
                   + '<i class="fa fa-share-alt" aria-hidden="true"></i></button>'

       $(cellID).append(shareButton);
    }
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
        url: '/make-share-request',
        data: JSON.stringify({"googleId": googleId}),
        contentType: 'application/json',
        success: function(result) {
            $("#spinner").hide();
            console.log(result);
            showShareRequestResult(result['status']);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}


function showShareRequestResult(status) {
    $('#shareModal').modal('hide');
    $('#feedbackModal').modal('show');

    if (status == 'sheet_accessible') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "A request has been sent to make your sheet available to everyone, subject to a quick review.";
        $("#feedbackModalBody").text(body);
    }
    else if (status == 'sheet_made_public') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "Your sheet is now available for everyone to see!";
        $("#feedbackModalBody").text(body);
    }
    else if (status == 'sheet_not_accessible') {
        const header = 'Uh oh...';
        $("#feedbackModalLabel").text(header);
        const body = "We couldn't access this sheet. Please make sure it has been shared with everyone (with the link) or with the email provided.";
        $("#feedbackModalBody").text(body);
    }
    else {
        const header = 'Uh oh...';
        $("#feedbackModalLabel").text(header);
        const body = "Something unexpected went wrong. Please try again later, and if you still have issues, contact our support.";
        $("#feedbackModalBody").text(body);
    }
}
