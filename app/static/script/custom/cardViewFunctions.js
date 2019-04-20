function getSheetData(id) {
    $("#spinner").show();
    const dataJson = JSON.stringify({"sheetID": id});

    return $.ajax({
        type: "POST",
        url: '/card-data',
        data: dataJson,
        contentType: 'application/json',
        success: function(result) {
            cards = new cardSet(result);
            $("#spinner").hide();
        },
        error: function(msg){
            console.log(msg);
            $("#spinner").hide();
        }
    });
};


function populateModalDropdowns(columnLookup) {

    // Create drop down selectors
    buildIndicatorList("primary-list", Object.values(columnLookup));
    buildIndicatorList("secondary-list", Object.values(columnLookup));
    buildIndicatorList("tertiary-list", Object.values(columnLookup), true);
    buildIndicatorList("modal-categories-list", Object.values(columnLookup), true);

    // Select the correct values in each drop down
    $('#primary-list option[value="' + columnLookup['languageOne'] + '"]').attr('selected', true);
    $('#secondary-list option[value="' + columnLookup['languageTwo'] + '"]').attr('selected', true);
    $('#modal-categories-list option[value="' + columnLookup['categories'] + '"]').attr('selected', true);
    if (columnLookup['languageThree'] === null) {
        $('#tertiary-list>option:eq(0)').attr('selected', true);
    } else {
        $('#tertiary-list option[value="' + columnLookup['languageThree'] + '"]').attr('selected', true);
    };
};

function buildIndicatorList(div, dataset, optional=false) {

	$("#" + div).empty();
    for (key in dataset) {
        if (dataset[key] !== null) {
            text = "<option value='" + dataset[key].toString() + "'>" + capitalizeFirstLetter(dataset[key].toString()) + "</option>";
            $("#" + div).append(text);
        }
    };

    if (optional) {
        text = "<option value='none'>None</option>";
        $("#" + div).prepend(text);
    };
};


function populateCards(cardsToDisplay) {

    // Get Text and Append to Cards
    for (let card in cardsToDisplay) {

        card = Number(card);

        // Generate ID tags
        let frontHtmlID = '#card' + String(card + 1) + ' .front';
        let primaryBackHtmlID = '#card' + String(card + 1) + '-back1';

        // Empty Old Values/Reset Font Sizes
        $(frontHtmlID).empty();
        $(primaryBackHtmlID).empty();

        // Append Words to Cards
        let frontText = '<p class="card-text" id="card' + String(card + 1) + '-ft">' + cardsToDisplay[card]['frontText'] + '</p>';

        $(frontHtmlID).append(frontText);
        $(primaryBackHtmlID).append('<p class="card-text" id="card' + String(card + 1) + '-bt1">' + cardsToDisplay[card]['primaryBackText'] + '</p>');

        // Set default size, then resize if needed
        $('#card'+ String(card + 1) + '-ft').css('font-size', defaultFontSize);
        $('#card' + String(card + 1) + '-bt1').css('font-size', defaultFontSize);
        $('#card'+ String(card + 1) + '-ft').css('font-size',
            getResizedFont(cardsToDisplay[card]['frontText']));
        $('#card' + String(card + 1) + '-bt1').css('font-size',
            getResizedFont(cardsToDisplay[card]['primaryBackText']));

        // If there is a third language, append that too
        if ('secondaryBackText' in cardsToDisplay[card]) {
            let secondaryBackHtmlID = '#card' + String(card + 1) + '-back2';
            $(secondaryBackHtmlID).empty();
            $(secondaryBackHtmlID).append('<p class="card-text" id="card' + String(card + 1) + '-bt2">' + cardsToDisplay[card]['secondaryBackText'] + '</p>');
            $('#card' + String(card + 1) + '-bt2').css('font-size', defaultFontSize);
            $('#card' + String(card + 1) + '-bt2').css('font-size',
                getResizedFont(cardsToDisplay[card]['secondaryBackText']));
        };
    };
};


/*-------------------------------------------------
CARD FUNCTIONALITY
-------------------------------------------------*/
function unflipCards() {
    for (var index = 1; index <= cardCount; ++index) {
        if ($('#card' + index).hasClass('flipped')) {
            $('#card' + index).toggleClass('flipped');
        };
    };
};


function checkButton(radioId) {
	allKeys = Object.keys(allData[ind_num]);

	if ($.inArray(year, allKeys) == -1) {
		// if currently selected year does not exist for new indicator, set year to latest year
		var yearToCheck = allKeys[allKeys.length - 1];
	} else {
		var yearToCheck = year;
	};

	// Set checks
};


function shuffle(array) {
    let currentIndex = array.length;
    let temporaryValue = null;
    let randomIndex = null;

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


/*-------------------------------------------------
UPDATE FUNCTIONS
-------------------------------------------------*/
function updateColumnMapping() {

    unflipCards();

    const indexMapping = {};
    indexMapping['languageOne'] = $("#primary-list").val();
    indexMapping['languageTwo'] = $("#secondary-list").val();
    indexMapping['languageThree'] = $("#tertiary-list").val();
    indexMapping['categories'] = $("#modal-categories-list").val();

    cards.saveIndexMap(indexMapping);

    $('#column-select').modal('hide');

    // Get Category and Language Lists
    const categories = cards.categoryList;
    buildIndicatorList("category-list", categories);

    setTimeout(function() {
        // Get Random numbers
        cards.refreshIdList();
        const cardsToDisplay = cards.nextCards;

        // Populate Cards
        populateCards(cardsToDisplay);
    }, 250);
}


function updateCategory() {
    // Unflip all Cards
    unflipCards();

    // Reset all Buttons
    for (let index = 1; index <= cardCount; ++index) {
        $('#card' + index + "-back :button").attr("disabled", false);
        $('#card' + index + '-back').css("background-color", "#E9C46A");
    };

    // Update Cards (delayed so answer is not revealed)
    setTimeout(function() {

        // Get and set selected category
        category = $("#category-list").val();
        cards.category = category;

        // Populate Cards
        cards.refreshIdList();
        populateCards(cards.nextCards);
    }, 250);
}


function refreshCards() {
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

        // Refresh Cards
        populateCards(cards.nextCards);
    }, 250);

    // Gives more satisfying click
    setTimeout(function() {
        $('#refresh-btn').removeClass('active');
    }, 500);
}


function updateRandomFlag() {
    value = $('input[type="radio"][name="or-radio"]:checked').val();
    if (value == 'random') {
        cards.randomFlag = true;
    } else {
        cards.randomFlag = false;
    };
    $('input[name="or-radio"]').removeClass('checked');
    $('input[name="or-radio"]:checked').addClass('checked');

    // Create New ID List
    cards.refreshIdList();
}


/*-------------------------------------------------
SCOREBOARD
-------------------------------------------------*/
function addCorrectScore(event) {
    event.stopPropagation();
    var cardID = $(this).parent().parent().attr('id');
    correct = correct + 1;
    $('#correct-count span').remove();
    $('#correct-count').append('<span id="cor-count">' + String(correct) + '</span>');
    $('#' + cardID + " :button").attr("disabled", true);
    $('#' + cardID).css("background-color", "#2A9D8F");

}


function addIncorrectScore(event) {
    event.stopPropagation();
    var cardID = $(this).parent().parent().attr('id');
    wrong = wrong + 1;
    $('#wrong-count span').remove();
    $('#wrong-count').append('<span id="wro-count">' + String(wrong) + '</span>');
    $('#' + cardID + " :button").attr("disabled", true);
    $('#' + cardID).css("background-color", "#E76F51");
}


/*-------------------------------------------------
FORMATTING FUNCTIONS
-------------------------------------------------*/
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

function showErrorModal() {
    $("#error-modal-header").empty();
    $("#error-modal-content").empty();

    errorInfo = cards.rawData['error'];
    const headerText = '<h4 style="text-align: center">' + errorInfo['modalHeader'] + '</h4>'


    const contentText = "<p>" + errorInfo['modalText'] + "</p>"

    $("#error-modal-header").append(headerText);
    $("#error-modal-header").append(contentText);

    $('#error-modal').modal('show');
}
