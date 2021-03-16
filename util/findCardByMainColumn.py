from models.CardSet import CardSet
from typing import Tuple, Dict, List

def findCardByMainColumn(term: str, cardSet: CardSet) -> Tuple[Dict[str, str], int]:
    for card in cardSet.cards:
        if card[cardSet.mainColumn] == term:
            return card, cardSet.cards.index(card)
        
    return {}, -1