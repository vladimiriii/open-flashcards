/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'sheets'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){
    $("#" + page).attr('class', 'active');
    createTable("requestSheets", ["reviewButton", "approveButton"]);
});
