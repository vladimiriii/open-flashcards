function showUserResultModal(eventType) {
    $('#shareModal').modal('hide');
    $('#feedbackModal').modal('show');

    if (eventType == 'Bought Graduate Package') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "User has been upgraded to a Graduate.";
        $("#feedbackModalBody").text(body);
    }
    else if (eventType == 'Bought Teacher Package') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "User has been upgraded to a Teacher.";
        $("#feedbackModalBody").text(body);
    }
    else if (eventType == 'Graduate Package Expired') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "User has been downgraded to an Undergraduate.";
        $("#feedbackModalBody").text(body);
    }
    else if (eventType == 'Teacher Package Expired') {
        const header = 'Success!';
        $("#feedbackModalLabel").text(header);
        const body = "User has been downgraded to an Undergraduate.";
        $("#feedbackModalBody").text(body);
    }
    else if (eventType == 'Block User') {
        const header = 'Success';
        $("#feedbackModalLabel").text(header);
        const body = "User has been blocked and will no longer be able to log in.";
        $("#feedbackModalBody").text(body);
    }
    else if (eventType == 'Unblock User') {
        const header = 'Success';
        $("#feedbackModalLabel").text(header);
        const body = "User has been unblocked and will now be able to log in.";
        $("#feedbackModalBody").text(body);
    }
    else {
        const header = 'Uh oh...';
        $("#feedbackModalLabel").text(header);
        const body = "Looks like you don't have the right permissions to do this.";
        $("#feedbackModalBody").text(body);
    }
}


function getUserColumnClass(column) {
    const lookup = {
        "User ID": "all",
        "Role": "all",
        "Email": "min-tablet-l",
        "Name": "min-tablet-p",
        "First Log In": "min-desktop",
        "Last Log In": "min-desktop",
        "Options": "all"
    };

    return lookup[column];
}
