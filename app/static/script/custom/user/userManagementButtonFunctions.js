function addGraduateUpgradeButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (role == 'Undergraduate') {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildGraduateButton(div, userId);
        }
    }
}


function buildGraduateButton(div, userId) {
    const cellId = "#opt-" + div + '-' + userId;
    const btn = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'Bought Graduate Package\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Convert to Graduate user">'
           + '<i class="fa fa-graduation-cap" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function addTeacherUpgradeButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (['Undergraduate', 'Graduate'].includes(role)) {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildTeacherButton(div, userId);
        }
    }
}


function buildTeacherButton(div, userId) {
    const cellId = "#opt-" + div + '-' + userId;
    const btn = '<button type="button" class="btn btn-outline-warning btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'Bought Teacher Package\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Convert to Teacher user">'
           + '<i class="fa fa-institution" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function addCancelPackageButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (['Graduate', 'Teacher'].includes(role)) {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildCancelPackageButton(div, userId, role);
        }
    }
}


function buildCancelPackageButton(div, userId, role) {
    const cellId = "#opt-" + div + '-' + userId;
    let user_event;
    if (role == "Graduate") {
        user_event = "Graduate Package Expired"
    }
    else if (role == "Teacher") {
        user_event = "Teacher Package Expired"
    }
    const btn = '<button type="button" class="btn btn-outline-danger btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'' + user_event + '\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Downgrade to Undergraduate user">'
           + '<i class="fa fa-ban" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}

function addBlockButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (!['Blocked', 'Super User', 'Guest'].includes(role)) {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildBlockButton(div, userId);
        }
    }
}


function buildBlockButton(div, userId) {
    const cellId = "#opt-" + div + '-' + userId;
    const user_event = "Block User";
    const btn = '<button type="button" class="btn btn-outline-primary btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'' + user_event + '\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Block user">'
           + '<i class="fa fa-lock" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function addUnblockButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (role == "Blocked") {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildUnblockButton(div, userId);
        }
    }
}


function buildUnblockButton(div, userId) {
    const cellId = "#opt-" + div + '-' + userId;
    const user_event = "Unblock User";
    const btn = '<button type="button" class="btn btn-outline-success btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'' + user_event + '\')"'
           + 'data-toggle="tooltip" data-placement="top" title="Unblock user">'
           + '<i class="fa fa-unlock" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function makeUserRequest(userId, user_event) {
    event.stopPropagation();
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-user-role',
        data: JSON.stringify({"userId": userId, "event": user_event}),
        contentType: 'application/json',
        success: function(result) {
            $("#spinner").hide();
            showUserResultModal(result['event']);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}
