/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'dashboard'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $("#" + page).attr('class', 'active');

    getSheetLists("publicSheets");
    getSheetLists("userSheets", ["shareButton"]);

});
