import os
from util.loadFile import loadFile
from typing import List, Dict, Union, Any
from .Card import Card


class CardSet:
    cards: List[Card]
    originPath: str
    columns: List[str]
    mainColumn: str
    # listValues: List[str]  # values to display in Listbox
    setData: Dict[str, Any]
    cardSetConfig: Dict[str, str]

    def __init__(self, filePath: str) -> None:
        self.originPath = filePath

        if os.path.isfile(filePath):
            self.cards, self.columns, cardSetConfig = loadFile(
                filePath=filePath)
            if len(self.columns) > 0:
                self.mainColumn = self.columns[0]

            # self.listValues = []
            # for card in self.cards:
            #     self.listValues.append(card.values[self.mainColumn])

            if not cardSetConfig:
                self.cardSetConfig = {'mainColumn': self.columns[0]}
                for card in self.cards:
                    card.setMainTerm(self.cardSetConfig['mainColumn'])
            else:
                self.cardSetConfig = cardSetConfig

    def updateCard(self, newValues: Dict[str, str], cardIndex: int):
        if Card is not None:
            self.cards[cardIndex].update(newValues=newValues, mainColumn=self.mainColumn)