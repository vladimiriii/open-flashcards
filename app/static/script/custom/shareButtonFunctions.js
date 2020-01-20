function addShareButton(div) {
    $("#" + div + " .table-row").on('click', function () {
            showShareButton(div, this.id, $(this).attr('data-value'));
    });
}

// SHARE BUTTON FUNCTIONS
function showShareButton(div, row_id, sheet_id) {
    $( "#" + div + "-share").remove();
    const cellID = "#" + String(row_id) + "-opt";
    if (!$("#" + String(row_id)).hasClass("selected")) {
        const share_button = '<button type="button" class="btn btn-outline-warning btn-sm confirm-col-btn" '
                   + 'id="' + div + '-share"'
                   + 'onclick="makeSheetPublic(' + sheet_id + ', event)">'
                   + '<i class="fa fa-share-alt" aria-hidden="true"></i></button>'

       $(cellID).append(share_button);
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


function submitShareRequest() {
    const googleId = $("#modalSubmit").val();
    $.ajax({
        type: "GET",
        url: '/make-share-request',
        data: {"googleId": googleId},
        success: function(result) {
            console.log(result);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}


function generateSheetLink(id) {
    const base_url = "https://docs.google.com/spreadsheets/d/";
    $.ajax({
        type: "GET",
        url: '/get-sheet-info',
        data: {"sheetId": id},
        success: function(result) {
            const url = base_url + result['googleId'];
            const html = 'Link to Spreadsheet: <a target="_blank" href=' + url + '>' + url + '</a>';
            $("#sheet-link").append(html);
            $("#modalSubmit").val(result['googleId']);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}
