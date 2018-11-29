/*-----------------------------------
Global Variables
-----------------------------------*/
var cardData,
    headers,
    catIndex,
    lanOneIndex,
    lanTwoIndex,
    lanThreeIndex,
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
    // Check Order Button	$('#' + yearToCheck).addClass('checked');
    $('input[id=ordered][name=or-radio]').prop("checked", true).change();

    // Get Card Data
    $.when(getSheetData()).done( function() {
        headers = cardData['headers'];

        // Populate Modal Drop Downs
        $('#column-select').modal('show');
        detectColumns();
        populateModalDropdowns();
    });

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

    // On Category Change
    $("#category-list").change(function(){
        // Unflip all Cards
        unflipCards();

        // Reset all Buttons
        for (var index = 1; index <= cardCount; ++index) {
            $('#card' + index + "-back :button").attr("disabled", false);
            $('#card' + index + '-back').css("background-color", "#E9C46A");
        };

        // Update Cards (delayed so answer is not revealed)
        setTimeout(function() {

            // Get Selected category
            category = $("#category-list").val();

            // Get IDs
            createIDList(category);
            getNextIds(cardCount);

            // Populate Cards
            populateCards(languages[0]);
        }, 250);
    });

    $('#refresh-btn').click(function() {
        $('#refresh-btn').toggleClass('active');

        // Unflip all Cards
        unflipCards();

        // Reset all buttons and colors
        for (var index = 1; index <= cardCount; ++index) {
            $('#card' + index + "-back :button").attr("disabled", false);
            $('#card' + index + '-back').css("background-color", "#E9C46A");
        };

        // Update Cards (delayed so answer is not revealed)
        setTimeout(function() {

            // Get Next IDs
            getNextIds(cardCount);

            // Populate Cards
            populateCards(languages[0]);
        }, 250);

        // Gives more satisfying click
        setTimeout(function() {
            $('#refresh-btn').removeClass('active');
        }, 500);
    });

    // Order Toggle
    $('#order-radio').on('change', 'input[name="or-radio"]', function() {
        value = $('input[type="radio"][name="or-radio"]:checked').val();
        if (value == 'random') {
            randomFlag = true;
        } else {
            randomFlag = false;
        };
		$('input[name="or-radio"]').removeClass('checked');
		$('input[name="or-radio"]:checked').addClass('checked');

        // Create New ID List
        createIDList(category);
    });

    // Keeping Score
    $('.correct-btn').click(function(event) {
        event.stopPropagation();
        var cardID = $(this).parent().parent().attr('id');
        correct = correct + 1;
        $('#correct-count span').remove();
        $('#correct-count').append('<span id="cor-count">' + String(correct) + '</span>');
        $('#' + cardID + " :button").attr("disabled", true);
        $('#' + cardID).css("background-color", "#2A9D8F");

    });
    $('.wrong-btn').click(function(event) {
        event.stopPropagation();
        var cardID = $(this).parent().parent().attr('id');
        wrong = wrong + 1;
        $('#wrong-count span').remove();
        $('#wrong-count').append('<span id="wro-count">' + String(wrong) + '</span>');
        $('#' + cardID + " :button").attr("disabled", true);
        $('#' + cardID).css("background-color", "#E76F51");
    });

    $('#reset-score').click(function() {
        correct = 0;
        wrong = 0;
        $('#correct-count span').remove();
        $('#wrong-count span').remove();
        $('#correct-count').append('<span id="cor-count">' + String(correct) + '</span>');
        $('#wrong-count').append('<span id="wro-count">' + String(wrong) + '</span>');
    });

    // Modal Accept Button
    $('#confirm-btn').click(function() {
        lanOneIndex = headers.indexOf($("#primary-list").val());
        lanTwoIndex = headers.indexOf($("#secondary-list").val());
        lanThreeIndex = headers.indexOf($("#tertiary-list").val());
        catIndex = headers.indexOf($("#modal-categories-list").val());
        $('#column-select').modal('hide');

        // Get Category and Language Lists
        var categories = getCategoryList(cardData['data']);
        languages = getLanguageList(headers);

        buildIndicatorList("category-list", categories);

        // Get Random numbers
        createIDList(category);
        getNextIds(cardCount);

        // Populate Cards
        populateCards(languages[0]);
    });
});
