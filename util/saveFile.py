import json
from util.log.log import LogLevel, consoleLog
from models.CardSet import CardSet
from models.Card import Card
from typing import List, Dict, Any

def saveFile(cardSet: CardSet, filePath: str) -> None:
    
    if filePath[-3:] == 'csv':
        consoleLog(LogLevel.WARNING, 'Can not save to .csv files' , '')
        return
    
    outputList: List[Dict[str, Any]] = [cardSet.cardSetConfig]
    
    for card in cardSet.cards:
        cardValues = card.values
        cardValues.update({'data': card.data}) # i hate python for this
        outputList.append(cardValues)
    
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(outputList))
