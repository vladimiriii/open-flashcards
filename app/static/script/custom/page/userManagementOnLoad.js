/*-----------------------------------
Global Variables
-----------------------------------*/
const page = 'users'

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    $("#" + page).attr('class', 'active');

    createTable("currentUsers",
                 ["graduateUpgradeButton",
                  "teacherUpgradeButton",
                  "cancelPackageButton",
                  "blockButton",
                  "unblockButton"]
    );

});
