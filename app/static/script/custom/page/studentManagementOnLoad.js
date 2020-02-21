/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'students'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $("#" + page).attr('class', 'active');
    
    getStudentListData("studentUsers", ["suspendButton", "deleteButton"]);

});
