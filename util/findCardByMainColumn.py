from models.CardSet import CardSet
from models.Card import Card
from typing import Tuple, Dict, List, Optional

def findCardByMainColumn(term: str, cardSet: CardSet) -> Tuple[Card, int]:
    for card in cardSet.cards:
        if card.mainTerm == term:
            return card, cardSet.cards.index(card)
    return Card(), -1