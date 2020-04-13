function getUserRole() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: '/check-user-role',
            success: (response) => {
                resolve(response['role']);
            },
            error: (response) => {
                reject(response);
            }
        })
    })
}


function getColumnIndices(tableData) {
    results = {}
    results['sheetId'] = tableData['columns'].indexOf("sheetId");
    results['googleId'] = tableData['columns'].indexOf("googleId");
    results['isOwner'] = tableData['columns'].indexOf("isOwner");
    results['status'] = tableData['columns'].indexOf("Status");

    return results
}
