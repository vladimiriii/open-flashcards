/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    getUserList("currentUsers",
                 ["graduateUpgradeButton",
                  "professorUpgradeButton",
                  "cancelPackageButton",
                  "blockButton"]
    );

});
