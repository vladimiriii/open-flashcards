/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'create'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function() {

    $("#" + page).attr('class', 'active');

    $('#submit-btn-opt-1').click(function () {
        const url = $('#url-input').val();
        let googleId = extractGoogleIdFromUrl(url);

        saveSheetMetadata(googleId);

    })

    $('#close-btn').click(closeModal)

});
