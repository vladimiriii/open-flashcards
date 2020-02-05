function showResultModal(status) {
    $('#shareModal').modal('hide');
    $('#feedbackModal').modal('show');

    if (status == 'Review Requested') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "A request has been sent to make your sheet available to everyone, subject to a quick review.";
        $("#feedbackModalBody").text(body);
    }
    else if (status == 'Public') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "Your sheet is now available for everyone to see!";
        $("#feedbackModalBody").text(body);
    }
    else if (status == 'Private') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "Your sheet is now only available for you to view.";
        $("#feedbackModalBody").text(body);
    }
    else if (status == 'sheet_not_accessible') {
        const header = 'Uh oh...';
        $("#feedbackModalLabel").text(header);
        const body = "We couldn't access this sheet. Please make sure it has been shared with everyone or with the email provided.";
        $("#feedbackModalBody").text(body);
    }
    else {
        const header = 'Uh oh...';
        $("#feedbackModalLabel").text(header);
        const body = "Something unexpected went wrong. Please try again later, and if you still have issues, please contact us.";
        $("#feedbackModalBody").text(body);
    }
}


function getColumnClass(column) {
    const lookup = {
        "Sheet Name": "all",
        "# of Cards": "min-tablet-p",
        "Views": "min-tablet-l",
        "Status": "min-tablet-p",
        "Last Modified": "min-desktop",
        "Options": "all",
        "User ID": "all",
        "Role": "all",
        "Email": "min-tablet-p",
        "Name": "all",
        "First Log In": "min-tablet-l",
        "Last Log In": "min-tablet-l"
    };

    return lookup[column];
}
