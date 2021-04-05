import os
from pathlib import Path
import mimetypes
import csv
import json
from typing import Dict, Tuple, List, Union
from util.exceptions.ParsingError import CSVParsingError
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

            # copy data from ready, because it can only be read once
            rowList = [row for row in reader]

            # first column in excel (bad variable name); these are the column names
            columns = [col.lower() for col in rowList[0]]

            for i, row in enumerate(rowList[1:]):
                try:
                    entry = Card(values={columns[i]: row[i] for i, c in enumerate(columns)},
                                 mainColumn=columns[0],
                                 data={'score': 0, 'lastStudied': None, 'index': i})
                except IndexError as e:
                    raise CSVParsingError('Some rows contain too few values')

                cardList.append(entry)

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
