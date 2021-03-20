import os
from pathlib import Path
import mimetypes
import csv
import json
from typing import Dict, Tuple, List, Union
from models.Card import Card


def loadFile(filePath: str) -> Tuple[List[Card], List[str], Dict[str, str]]:
    cardList: List[Card] = []
    columns: List[str] = []
    cardSetConfig: Dict[str, str] = {}

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
                columns.append(rowList[i][0].lower())

            for cardName in rowList[0]:
                # basicly the index of the card in the excel table
                index = rowList[0].index(cardName)
                if index == 0:
                    continue  # skip first column because it contains the column names
                entry = {}
                for row in rowList:
                    # for every coloum name add the card data to the entry
                    entry.update({row[0]: row[index]})

                # add that card to the card set
                cardList.append(Card(values=entry))

            for i, card in enumerate(cardList):
                if not 'data' in columns:
                    card.data = {'score': 0, 'lastStudied': None, 'index': i}

    elif '.json' in extensions or '.fsc' in extensions:
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            jsonObject = json.loads(inputFile.read())

            if 'mainColumn' in jsonObject[0]:
                cardSetConfig = jsonObject.pop(0)
            else:
                for i, cardDict in enumerate(jsonObject):
                    if 'mainColumn' in cardDict:
                        cardSetConfig = jsonObject.pop(i)

            for i, cardDict in enumerate(jsonObject):
                data = cardDict.get('data', None)
                if data is not None:
                    cardDict.pop('data')
                else:
                    data = {'score': 0, 'lastStudied': None, 'index': i}

                cardList.append(Card(values=cardDict,
                                     mainColumn=cardSetConfig.get(
                                         'mainColumn', None),
                                     data=data))

            # feels kinda weird because it's only looking at the first card and
            # takes the columns from that instead of check the other cards...
            columns = list(cardList[0].values.keys())

    return cardList, columns, cardSetConfig
