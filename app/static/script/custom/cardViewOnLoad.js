/*-----------------------------------
Global Variables
-----------------------------------*/
var cards,
    catIndex,
    languages;

var category = "All",
    randomFlag = false,
    correct = 0,
    wrong = 0,
    cardCount = 4,
    allIds = [],
    defaultFontSize = 40,
    currentIds;

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){
    const indices = {'langaugeOne': null, 'langaugeTwo': null, 'langaugeThree': null, 'categories': null}

    // Check Random Button
    $('input[id=random][name=or-radio]').prop("checked", true).change();

    // Get Card Data
    $.when(getSheetData()).done( function() {

        // Populate Modal Drop Downs
        $('#column-select').modal('show');
        let columnLookup = cards.suggestColumns();
        populateModalDropdowns(columnLookup);

    });

    // Modal Accept Button
    $('#confirm-btn').click(updateColumnMapping);

    // Initialize Scoreboard
    $('#correct-count').append('<span id="cor-count">0</span>');
    $('#wrong-count').append('<span id="wro-count">0</span>');

    // Flip cards on click
    $('#card1').click(function() {
        $('#card1').toggleClass('flipped');
    });

    $('#card2').click(function() {
        $('#card2').toggleClass('flipped');
    });

    $('#card3').click(function() {
        $('#card3').toggleClass('flipped');
    });

    $('#card4').click(function() {
        $('#card4').toggleClass('flipped');
    });

    // Main Card Options
    $("#category-list").change(updateCategory);
    $('#refresh-btn').click(refreshCards);
    $('#order-radio').on('change', 'input[name="or-radio"]', updateRandomFlag);

    // Keeping Score
    $('.correct-btn').click(addCorrectScore);
    $('.wrong-btn').click(addIncorrectScore);

    $('#reset-score').click(function() {
        correct = 0;
        wrong = 0;
        $('#correct-count span').remove();
        $('#wrong-count span').remove();
        $('#correct-count').append('<span id="cor-count">' + String(correct) + '</span>');
        $('#wrong-count').append('<span id="wro-count">' + String(wrong) + '</span>');
    });


});
