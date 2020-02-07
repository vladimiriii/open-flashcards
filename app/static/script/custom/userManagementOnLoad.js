/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    getUserList("currentUsers",
                 ["graduateUpgradeButton",
                  "teacherUpgradeButton",
                  "cancelPackageButton",
                  "blockButton",
                  "unblockButton"]
    );

});
