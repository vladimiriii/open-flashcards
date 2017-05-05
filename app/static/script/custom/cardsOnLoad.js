/*-----------------------------------
Global Variables
-----------------------------------*/
var cardData,
    catIndex,
    lanOneIndex,
    lanTwoIndex,
    lanThreeIndex,
    primaryLanguage,
    languages;


var category = "All",
    correct = 0,
    wrong = 0,
    cardCount = 4,
    allIds = [],
    defaultFontSize = 40,
    currentIds;

/*-----------------------------------
Functions
-----------------------------------*/
function getSheetData() {
    $("#spinner").show();
    return $.ajax({
        type: "GET",
        url: '/card-data',
        contentType: 'application/json',
        success: function(result) {
            cardData = result;
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};

// Build list of indicators
function buildIndicatorList(div, dataset) {
	$("#" + div).empty();
    for (key in dataset) {
        text = "<option value='" + dataset[key] + "'>" + capitalizeFirstLetter(dataset[key]) + "</option>";
        $("#" + div).append(text);
    };
};

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);

};

function getResizedFont(text, language) {
    var fontSize;
    if (text.length > 8) {
        fontSize = defaultFontSize - ((text.length - 8) * 2);
    };
    return Math.max(fontSize, 16);
};

function getCategoryList(array) {
    var finalList = ["All"];
    var cat;

    for (var index = 0; index < array.length; ++index) {
        cat = array[index][catIndex];
        if ($.inArray(cat, finalList) == -1) {
            finalList.push(cat);
        };
    };
    return finalList;
};

function getLanguageList(array) {
    var languages = [];
    languages.push(array[lanOneIndex]);
    languages.push(array[lanTwoIndex]);

    if (array.length == 4) {
        languages.push(array[lanThreeIndex]);
    };
    return languages
}

function createIDList(cat) {
    // Reinitialize allIds
    allIds = [];
    var array = cardData['data']

    // Filter data for the category
    if (cat != "All") {
        var array = array.filter( function(itm) {
            return itm[catIndex] == cat;
        });
    };
    for (var i = 0; i < array.length; ++i) {
        var index = cardData['data'].indexOf(array[i]);
        if (index != -1) {
            allIds.push(index);
        };
    };

    // Randomize Array
    allIds = shuffle(allIds);
};

function shuffle(array) {
  var currentIndex = array.length,
      temporaryValue,
      randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
    };

  return array;
};

function getRandomIds(entries) {
    var idsRemaining = allIds.length;

    if (idsRemaining >= entries) {
        currentIds = allIds.slice(0, entries);
        allIds = allIds.slice(entries, allIds.length);
    } else {
        currentIds = allIds.slice(0);
        var addIDsNeeded = entries - idsRemaining;
        createIDList(category);
        while (currentIds.length < entries) {
            var newValue = allIds[0];
            // Check if item is already selected
            if (currentIds.indexOf(newValue) == -1) {
                currentIds.push(newValue);
                allIds.splice(0, 1);
            } else {
                // If it is, move item to end of array
                allIds.push(allIds.splice(0, 1)[0]);
            };
        };
    };
};

function populateCards(front) {
    var id,
        araText,
        engText,
        traText,
        record,
        cardNo,
        htmlID;

    var array = cardData['data'];
    var headers = cardData['headers'];

    // Determine Front and Back entries
    var entries = languages.slice(0);
    var indexToRemove = entries.indexOf(front);
    if (indexToRemove > -1) {
        entries.splice(indexToRemove, 1);
    };
    var frontIndex = headers.indexOf(front);
    var backIndices = [headers.indexOf(entries[0]), headers.indexOf(entries[1])];

    // Get Text and Append to Cards
    for (var index = 0; index < cardCount; ++index) {
        id = currentIds[index];
        record = array[id];
        frontText = record[frontIndex];
        backText1 = record[backIndices[0]];

        // Generate ID tags
        frontHtmlID = '#card' + String(index + 1) + ' .front';
        back1HtmlID = '#card' + String(index + 1) + '-back1';

        // Empty Old Values/Reset Font Sizes
        $(frontHtmlID).empty();
        $(back1HtmlID).empty();

        // Append Words to Cards
        $(frontHtmlID).append('<p class="card-text" id="card' + String(index + 1) + '-ft">' + frontText + '</p>');
        $(back1HtmlID).append('<p class="card-text" id="card' + String(index + 1) + '-bt1">' + backText1 + '</p>');

        // Set default size, then resize if needed
        $('#card'+ String(index + 1) + '-ft').css('font-size', defaultFontSize);
        $('#card' + String(index + 1) + '-bt1').css('font-size', defaultFontSize);
        $('#card'+ String(index + 1) + '-ft').css('font-size', getResizedFont(frontText));
        $('#card' + String(index + 1) + '-bt1').css('font-size', getResizedFont(backText1));

        // If there is a third language, append that too
        if (languages.length == 3) {
            backText2 = record[backIndices[1]];
            back2HtmlID = '#card' + String(index + 1) + '-back2';
            $(back2HtmlID).empty();
            $(back2HtmlID).append('<p class="card-text" id="card' + String(index + 1) + '-bt2">' + backText2 + '</p>');
            $('#card' + String(index + 1) + '-bt2').css('font-size', defaultFontSize);
            $('#card' + String(index + 1) + '-bt2').css('font-size', getResizedFont(backText2));
        };
    };
};

// Unflip all Cards
function unflipCards() {
    for (var index = 1; index <= cardCount; ++index) {
        if ($('#card' + index).hasClass('flipped')) {
            $('#card' + index).toggleClass('flipped');
        };
    };
};

/*-----------------------------------
On Page Load
-----------------------------------*/
$(document).ready(function(){

    // Get Card Data
    $.when(getSheetData()).done( function() {
        catIndex = (cardData['headers'].length) - 1;
        lanOneIndex = 0;
        lanTwoIndex = 1;
        lanThreeIndex = 2;

        // Get Category and Language Lists
        var categories = getCategoryList(cardData['data']);
        languages = getLanguageList(cardData['headers']);
        primaryLanguage = cardData['headers'][lanOneIndex];

        // Populate Dropdowns
        buildIndicatorList("language-list", languages);
        $("#language-list").val(primaryLanguage);
        buildIndicatorList("category-list", categories);

        // Initialize Scoreboard
        $('#correct-count').append('<span id="cor-count">0</span>');
        $('#wrong-count').append('<span id="wro-count">0</span>');

        // Get Random numbers
        createIDList(category);
        getRandomIds(cardCount);

        // Populate Cards
        populateCards(primaryLanguage);
    });

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

    // On Language Change
    $("#language-list").change(function(){

        // Unflip all Cards
        unflipCards();

        // Reset all Buttons
        for (var index = 1; index <= cardCount; ++index) {
            $('#card' + index + "-back :button").attr("disabled", false);
            $('#card' + index + '-back').css("background-color", "#E9C46A");
        };

        // Update Cards (delayed so answer is not revealed)
        setTimeout(function() {

            // Get Selected Language
            primaryLanguage = $("#language-list").val();

            // Get IDs
            createIDList(category);
            getRandomIds(cardCount);

            // Populate Cards
            populateCards(primaryLanguage);
        }, 250);
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
            getRandomIds(cardCount);

            // Populate Cards
            populateCards(primaryLanguage);
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

            // Get Selected Language
            primaryLanguage = $("#language-list").val();

            // Get Random IDs
            getRandomIds(cardCount);

            // Populate Cards
            populateCards(primaryLanguage);
        }, 250);

        // Gives more satisfying click
        setTimeout(function() {
            $('#refresh-btn').removeClass('active');
        }, 500);
    });

    // Keeping Score
    $('.correct-btn').click(function() {
        event.stopPropagation();
        var cardID = $(this).parent().parent().attr('id');
        correct = correct + 1;
        $('#correct-count span').remove();
        $('#correct-count').append('<span id="cor-count">' + String(correct) + '</span>');
        $('#' + cardID + " :button").attr("disabled", true);
        $('#' + cardID).css("background-color", "#2A9D8F");

    });
    $('.wrong-btn').click(function() {
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

});
