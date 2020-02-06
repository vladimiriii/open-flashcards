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
           + 'onclick="makeUserRequest(\'' + userId + '\', \'Bought Graduate Package\')">'
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
           + 'onclick="makeUserRequest(\'' + userId + '\', \'Bought Teacher Package\')">'
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
    const btn = '<button type="button" class="btn btn-outline-primary btn-sm confirm-col-btn" '
           + 'onclick="makeUserRequest(\'' + userId + '\', \'' + user_event + '\')">'
           + '<i class="fa fa-ban" aria-hidden="true"></i></button>'
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
            console.log(result);
            // showResultModal(result['status']);
        },
        error: function(msg){
            console.log(msg);
        }
    })
}
