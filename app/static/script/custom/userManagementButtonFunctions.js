function addGraduateButtons(div, tableData, userIdIndex, roleIndex) {
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
           + 'onclick="makeGraduateRequest(\'' + userId + '\')">'
           + '<i class="fa fa-level-up" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function makeGraduateRequest(userId) {
    event.stopPropagation();
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-user-role',
        data: JSON.stringify({"userId": userId, "event": "Bought Graduate Package"}),
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

function addCancelPackageButtons(div, tableData, userIdIndex, roleIndex) {
    for (rowIndex in tableData) {
        const role = tableData[rowIndex][roleIndex]
        if (['Graduate', 'Professor'].includes(role)) {
            const userId = String(tableData[rowIndex][userIdIndex]);
            buildCancelPackageButton(div, userId);
        }
    }
}


function buildCancelPackageButton(div, userId) {
    const cellId = "#opt-" + div + '-' + userId;
    const btn = '<button type="button" class="btn btn-outline-primary btn-sm confirm-col-btn" '
           + 'onclick="makeCancelPackageRequest(\'' + userId + '\')">'
           + '<i class="fa fa-level-down" aria-hidden="true"></i></button>'
   $(cellId).append(btn);
}


function makeCancelPackageRequest(userId) {
    event.stopPropagation();
    $("#spinner").show();
    $.ajax({
        type: "POST",
        url: '/update-user-role',
        data: JSON.stringify({"userId": userId, "event": "Graduate Package Expired"}),
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
