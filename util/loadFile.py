import os
from pathlib import Path
import mimetypes
import csv
import json
from typing import Dict, Tuple, List


def loadFile(filePath: str) -> Tuple[List[Dict[str, str]], list]:
    cardsList = []
    columns = []
    mimetypes.add_type('FloraStudy Card-File', '.fsc')
    extensions = [s for s in Path(
        filePath).suffixes if s in mimetypes.types_map]

    if '.csv' in extensions:
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            reader = csv.reader(inputFile)
            rowList = []

            for row in reader:
                # copy data from ready, because it can only be read once
                rowList.append(row)

            for i in range(len(rowList)):
                # first column in excel (bad var name); these are the column names
                columns.append(rowList[i][0])

            for cardName in rowList[0]:
                # basicly the index of the card in the excel table
                index = rowList[0].index(cardName)
                if index == 0:
                    continue  # skip first column because it contains the column names
                entry = {}
                for row in rowList:
                    # for every coloum name add the card data to the entry
                    entry.update({row[0]: row[index]})

                cardsList.append(entry)  # add that entry to the card set

    elif '.json' in extensions or '.fsc' in extensions:
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            jsonString = inputFile.read()
            cardsList = json.loads(jsonString)
            columns = list(cardsList[0].keys()) # feels kinda weird because it's only looking at the first card and 
                                                # takes the columns from that instead of check the other cards...

    # else:
    #     # log
    #     print('Unknown file type')

    return cardsList, columns
