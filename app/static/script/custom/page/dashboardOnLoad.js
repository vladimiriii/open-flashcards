/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'dashboard'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $("#" + page).attr('class', 'active');

    createTable("publicSheets", ["viewButton"]);
    createTable("userSheets", ["viewButton", "shareButton", "cancelButton", "privateButton"]);

});
