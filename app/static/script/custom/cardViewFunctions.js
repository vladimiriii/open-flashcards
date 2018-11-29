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
function buildIndicatorList(div, dataset, optional=false) {
	$("#" + div).empty();
    for (key in dataset) {
        text = "<option value='" + dataset[key].toString() + "'>" + capitalizeFirstLetter(dataset[key].toString()) + "</option>";
        $("#" + div).append(text);
    };

    if (optional) {
        text = "<option value='none'>None</option>";
        $("#" + div).prepend(text);
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

    if (catIndex != -1) {
        for (var index = 0; index < array.length; ++index) {
            cat = array[index][catIndex];
            if ($.inArray(cat, finalList) == -1) {
                finalList.push(cat);
            };
        };
    };
    return finalList;
};

function getLanguageList(array) {
    var languages = [];
    languages.push(array[lanOneIndex]);
    languages.push(array[lanTwoIndex]);

    if (lanThreeIndex > 0) {
        languages.push(array[lanThreeIndex]);
    };
    return languages
}

function createIDList(cat) {
    // Reinitialize all IDs
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
    if (randomFlag) {
        allIds = shuffle(allIds);
    };
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

function getNextIds(entries) {
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


function detectColumns() {

    // Take data row as an example and determine string columns
    var sampleRow = cardData['data'][0];
    var colIndices = [];
    for (n in cardData['headers']) {
        colIndices.push(n);
    };

    // Check header names for category column
    var catFound = false;
    for (hdrIdx in cardData['headers']) {
        var header = cardData['headers'][hdrIdx].toLowerCase();
        if (header.indexOf('cat') != -1) {
            catIndex = Number(hdrIdx);
            catFound = true;
            break;
        };
    };

    // If that doesn't work, look at column values
    if (!catFound) {
        // Loop through all columns, get unique value count
        // Column with lowest unique value count will be guessed as category column
        uniqueVals = [];
        for (rowIndex in cardData['data']) {
            row = cardData['data'][rowIndex];
            for (i in colIndices) {
                // Initialize array of arrays
                if (rowIndex == 0){
                    uniqueVals[i] = [];
                };
                // console.log(uniqueVals);
                if (uniqueVals[i].indexOf(row[i]) == -1) {
                    uniqueVals[i].push(row[i]);
                };
            };
        };

        // Count Values and get max and min
        counts = [];
        for (list in uniqueVals) {
            counts.push(uniqueVals[list].length);
        };
        var minValue = Math.min.apply(null, counts);
        var maxValue = Math.max.apply(null, counts);

        // If min is less than max, assume min column is category column
        // If not, than assume there is not category column
        if (minValue < maxValue) {
            catIndex = Number(colIndices[counts.indexOf(minValue)]);
            catFound = true;
        };
    };

    // Remove Category Column (if found)
    if (catFound) {
        colIndices.splice(catIndex, 1);
    };

    // Remove ID Columns (if any, and if there are still enough columns)
    for (ind in colIndices) {
        var header = cardData['headers'][colIndices[ind]].toLowerCase();
        // Need at least two headers for languages
        if (header.indexOf('id') != -1 && colIndices.length > 2) {
            colIndices.splice(ind, 1);
        };
    };

    // Assign Remaining Columns
    lanOneIndex = Number(colIndices[0]);
    lanTwoIndex = Number(colIndices[1]);
    if (colIndices.length > 2) {
        lanThreeIndex = Number(colIndices[2]);
    } else {
        lanThreeIndex = -1;
    };
};

function populateModalDropdowns() {
    buildIndicatorList("primary-list", headers);
    buildIndicatorList("secondary-list", headers);
    buildIndicatorList("tertiary-list", headers, true);
    buildIndicatorList("modal-categories-list", headers, true);
    $('#primary-list>option:eq(' + lanOneIndex + ')').prop('selected', true);
    $('#secondary-list>option:eq(' + lanTwoIndex + ')').prop('selected', true);
    $('#modal-categories-list>option:eq(' + (catIndex + 1).toString() + ')').prop('selected', true);
    if (headers.length == 3) {
        $('#tertiary-list>option:eq(0)').prop('selected', true);
    } else if (headers.length > 3) {
        $('#tertiary-list>option:eq(' + (lanThreeIndex + 1).toString() + ')').prop('selected', true);
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
