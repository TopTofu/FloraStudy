import os
from util.loadFile import loadFile
from typing import List, Dict


class CardSet:

    cards: List[Dict[str, str]]
    originPath: str
    columns: List[str]
    mainColumn: str
    listValues: List[str]  # values to display in Listbox

    def __init__(self, filePath: str) -> None:
        self.originPath = filePath

        if os.path.isfile(filePath):
            self.cards, self.columns = loadFile(filePath=filePath)
            if len(self.columns) > 0:
                self.mainColumn = self.columns[0]

            self.listValues = []
            for card in self.cards:
                self.listValues.append(card[self.mainColumn])
    
    def updateCard(self,  newCard: Dict[str, str], cardIndex: int):
        self.cards[cardIndex] = newCard
        self.listValues[cardIndex] = newCard[self.mainColumn]
