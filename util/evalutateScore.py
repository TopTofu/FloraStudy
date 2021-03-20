from models.Card import Card

def evaluateScore(card: Card, rating: str) -> int:
    
    initialScore = card.data['score']

    if rating in ('EASYBUTTON', '1'):
        return initialScore + 1
    
    if rating in ('HARDBUTTON', '3'):
        return initialScore - 1
    
    return initialScore