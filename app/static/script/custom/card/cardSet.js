class cardSet {

    constructor(cardData) {
        this.rawData = cardData;
        this.indexMapping = null;
        this.idList = [];
        this.randomFlag = true;
        this.cardsToDisplay = 4;
        this.category = 'all';
        this.fulListLength = null;
    }

    dataFound() {
        if ('error' in this.rawData) {
            return false;
        }
        else {
            return true;
        }
    }


    suggestColumns() {

        const indexMapping = {};
        const availableIndices = [...Array(this.rawData['headers'].length).keys()];

        // Check header names for category column
        let categoriesProvided = false;
        let headerText;
        for (let headerIndex in this.rawData['headers']) {
            headerText = this.rawData['headers'][headerIndex];
            if (headerText.toLowerCase().indexOf('cat') != -1) {
                indexMapping['categories'] = headerText;
                categoriesProvided = true;
                break;
            }
        }

        // If that doesn't work, look at column values
        if (!categoriesProvided) {
            // Loop through all columns, get unique value count
            // Column with lowest unique value count will be guessed as category column
            const uniqueVals = [];
            let row;
            for (let rowIndex in this.rawData['data']) {
                row = this.rawData['data'][rowIndex];
                for (let i in this.rawData['headers']) {
                    // Initialize array of arrays
                    if (rowIndex == 0){
                        uniqueVals[i] = [];
                    }
                    if (uniqueVals[i].indexOf(row[i]) == -1) {
                        uniqueVals[i].push(row[i]);
                    }
                }
            }

            // Count Values and get max and min
            const counts = [];
            for (let list in uniqueVals) {
               counts.push(uniqueVals[list].length);
            }
            const minValue = Math.min.apply(null, counts);
            const maxValue = Math.max.apply(null, counts);

            // If min is less than max, assume min column is category column
            // If not, than assume there is no category column
            if (minValue < maxValue) {
               indexMapping['categories'] = this.rawData['headers'][counts.indexOf(minValue)];
               categoriesProvided = true;
            }
        }

        // Remove Category Column from available indicies (if found)
        if (categoriesProvided) {
           availableIndices.splice(this.rawData['headers'].indexOf(indexMapping['categories']), 1);
        }

        // Remove ID Columns (if any, and if there are still enough columns)
        let header;
        for (let headerIndex in this.rawData['headers']) {
           header = this.rawData['headers'][headerIndex];
           // Need at least two headers for languages
           if (header.toLowerCase().indexOf('id') != -1 && availableIndices.length > 2) {
               availableIndices.splice(headerIndex, 1);
           }
        }

        // Assign Remaining Columns
        indexMapping['languageOne'] = this.rawData['headers'][availableIndices[0]];
        indexMapping['languageTwo'] = this.rawData['headers'][availableIndices[1]];
        if (availableIndices.length > 2) {
           indexMapping['languageThree'] = this.rawData['headers'][availableIndices[2]];
        } else {
           indexMapping['languageThree'] = null;
        }

        // Return results
        return indexMapping;
    }


    saveIndexMap(map) {
        const result = {};
        result['languageOne'] = this.rawData['headers'].indexOf(map['languageOne']);
        result['languageTwo'] = this.rawData['headers'].indexOf(map['languageTwo']);
        result['languageThree'] = this.rawData['headers'].indexOf(map['languageThree']);
        result['categories'] = this.rawData['headers'].indexOf(map['categories']);
        this._indexMapping = result;
    }


    refreshIdList() {

        let allIds;
        if (this._category != 'all') {
            allIds = [];
            for (let rowIndex in this.rawData['data']) {
                if (this.rawData['data'][rowIndex][this._indexMapping['categories']] == this._category) {
                    allIds.push(rowIndex);
                }
            }
        } else {
          allIds = Object.keys(this.rawData['data']);
        }

        if (this._randomFlag) {
            allIds = shuffle(allIds);
        }
        this.idList = allIds;
        this._fullListLength = allIds.length;
    }


    get categoryList() {

        const finalList = ["All"];
        let category;

        if (this._indexMapping['categories'] != -1) {
            for (let row in this.rawData['data']) {
                category = this.rawData['data'][row][this._indexMapping['categories']];
                if (finalList.indexOf(category) == -1) {
                    finalList.push(category);
                };
            };
        };
        return finalList;
    }


    get nextCards() {

        const idsRemaining = this.idList.length;
        let currentIds;

        if (idsRemaining >= this._cardsToDisplay) {
            currentIds = this.idList.slice(0, this._cardsToDisplay);
            this.idList = this.idList.slice(this._cardsToDisplay, idsRemaining);
        }
        else {
            currentIds = this.idList.slice(0);
            this.refreshIdList();

            let newValue;
            while (currentIds.length < this._cardsToDisplay) {
                newValue = this.idList[0];

                // Make sure we don't repeat a card unless there are not enough cards
                if (this._fullListLength == 1) {
                    currentIds.push(newValue);
                }
                else if (currentIds.indexOf(newValue) == -1 || this._fullListLength <= this._cardsToDisplay) {
                    currentIds.push(newValue);
                    this.idList.splice(0, 1);
                } else {
                    this.idList.push(this.idList.splice(0, 1)[0]);
                }
            }
        }

        // Get Text and Append to Cards
        const results = [];
        let rawRecord;
        for (let id in currentIds) {
            let textRecord = {};
            rawRecord = this.rawData['data'][currentIds[id]];
            textRecord['frontText'] = rawRecord[this._indexMapping['languageOne']];
            textRecord['primaryBackText'] = rawRecord[this._indexMapping['languageTwo']];

            // If there is a third language, append that too
            if (this._indexMapping['languageThree'] != -1) {
                textRecord['secondaryBackText'] = rawRecord[this._indexMapping['languageThree']];
            }

            results.push(textRecord);
        }
        return results;
    }


    set category(cat) {
        this._category = cat;
    }


    set cardsToDisplay(value) {
        this._cardsToDisplay = value;
    }


    set randomFlag(flag) {
        this._randomFlag = flag;
    }

}

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
