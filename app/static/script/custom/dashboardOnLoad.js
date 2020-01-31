/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'dashboard'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $("#" + page).attr('class', 'active');

    getSheetLists("publicSheets", ["viewButton"]);
    getSheetLists("userSheets", ["viewButton", "shareButton", "cancelButton", "privateButton"]);

});
