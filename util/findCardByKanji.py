from typing import Tuple, Dict, List

def findCardByKanji(term: str, cards: List[Dict[str, str]], mainColumn: str) -> Tuple[Dict[str, str], int]:
    for card in cards:
        if card[mainColumn] == term:
            return card, cards.index(card)
        
    return {}, -1