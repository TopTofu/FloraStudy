import json
from models.CardSet import CardSet
from models.Card import Card
from typing import List, Dict, Any

def saveFile(cardSet: CardSet, filePath: str) -> None:
    
    outputList: List[Dict[str, Any]] = [cardSet.cardSetConfig]
    
    for card in cardSet.cards:
        cardValues = card.values
        cardValues.update(card.data) # i hate python for this
        outputList.append(cardValues)
    
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(outputList))
