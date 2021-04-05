import os
from util.loadFile import loadFile
from typing import List, Dict, Union, Any
from .Card import Card


class CardSet:
    cards: List[Card]
    originPath: str
    columns: List[str]
    mainColumn: str
    setData: Dict[str, Any]
    cardSetConfig: Dict[str, Any]

    def __init__(self, filePath: str) -> None:
        self.originPath = filePath

        if os.path.isfile(filePath):
            self.cards, self.columns, cardSetConfig = loadFile(
                filePath=filePath)

            self.cardSetConfig = self.createCardSetConfigIfNotEmpty(
                cardSetConfig)

            if self.cardSetConfig.get('mainColumn', None) is not None:
                self.mainColumn = self.cardSetConfig['mainColumn']

    # maybe swap cardIndex with card?
    def updateCard(self, newValues: Dict[str, str], cardIndex: int):
        self.cards[cardIndex].update(
            newValues=newValues, mainColumn=self.mainColumn)

    def updateCardData(self, newData: Dict[str, Any], card: Card):
        if Card is not None:
            self.cards[self.cards.index(card)].updateData(newData)

    def createCardSetConfigIfNotEmpty(self, cardSetConfig: Dict[str, Any]) -> Dict[str, Any]:
        if not cardSetConfig:
            cardSetConfig = {'mainColumn': self.columns[0],  # create now default cardSet config is None is given
                             'promptColumns': [{self.columns[0]: 12}],
                             'revealColumns': [{self.columns[1]: 12}]
                             }
            for card in self.cards:
                # sets the main term of the cards once the config is created
                # because the mainColumn is only stored in the cardSetConfig
                card.setMainTerm(cardSetConfig['mainColumn'])

        return cardSetConfig
