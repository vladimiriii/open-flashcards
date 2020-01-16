function extractGoogleIdFromUrl(url) {
	let googleId;

	if (url.includes('spreadsheets')) {
		// Method #1
		const regexOne = /(?:spreadsheets\/d\/)[a-zA-Z0-9-_]+/gm;
		const regexOutput = regexOne.exec(url);
		googleId = regexOutput[0].substring(15);
	}
	else if(url.includes('drive')) {
		// Method #2
		const regexTwo = /(?:\/open\?id=)[a-zA-Z0-9-_]+/gm;
		const regexOutput = regexTwo.exec(url);
		googleId = regexOutput[0].substring(9);
	}
	else {
		googleId = null;
	}

	return googleId;
}


function saveSheetMetadata(googleId) {
    $("#spinner").show();

    $.ajax({
        type: "POST",
        url: "./register-sheet",
        data: googleId,
        contentType: "text/plain",
        dataType: "text",
        success: function(result) {
            // Parse json string
            let response = JSON.parse(result);
            generateResponseModal(response);
        },
        error: function(msg) {
            $(postTo).append(msg);
        }
    });
}


function generateResponseModal(response) {
    const status = response['status'];
    $("#modal-header").empty();
    $("#modal-body").empty();
    $("#success-btn").remove();

    const headerText = '<h4>' + responseMap[status]['header'] + '</h4>';
    $("#modal-header").append(headerText);
    const bodyText = "<p>" + responseMap[status]['body'] + "</p>";
    $("#modal-body").append(bodyText);

    if (['sheet_imported', 'sheet_already_imported'].includes(status)) {
        const sheetId = response['sheetId'];
        const viewButton = '<a href="./flashcards/' + sheetId + '"><button type="button" class="btn btn-outline-success" id="success-btn">View Cards</button></a>';
        $("#modal-footer").prepend(viewButton);
    }

    $('#confirmation-modal').modal('show');
    $("#spinner").hide();
}


function closeModal() {
    $('#confirmation-modal').modal('hide');
}


responseMap = {
    'sheet_imported': {
        'header': "Success!",
        'body': "Your sheet has been successfully imported."
    },
    'sheet_not_exist': {
        'header': "Oops!",
        'body': "We couldn't find your sheet. Please check the URL is correct, and that you have permission to view this sheet with the account you used to sign in."
    },
    'invalid_url': {
        'header': "Oops!",
        'body': "Looks like the URL provided was not the correct format. Please double check and try again."
    },
    'unknown_error': {
        'header': "Oops!",
        'body': "Something unexpected went wrong. Please try again, and if the problem persists get in touch."
    },
    'sheet_already_imported': {
        'header': "Already Done!",
        'body': "Looks like you have already imported this sheet!"
    }
};
