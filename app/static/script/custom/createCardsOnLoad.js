/*-----------------------------------
Global Variables
-----------------------------------*/


/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function() {

    $('#submit-btn-opt-1').click(function () {
        const url = $('#url-input').val();
        let googleId = extractGoogleIdFromUrl(url);

        saveSheetMetadata(googleId);

    })

    $('#close-btn').click(closeModal)

});
