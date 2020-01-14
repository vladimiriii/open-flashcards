/*-----------------------------------
Global Variables
-----------------------------------*/

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $.when(getSheetLists({"publicSheets": false, "userSheets": true})).done(function() {

        addViewButton('user-cards');
        addShareButton('user-cards');

    })

});
