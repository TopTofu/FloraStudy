import PySimpleGUI as gui
from ..models.CardSet import CardSet

def init(cardSet: CardSet) -> CardSet:
    layout = [[]]
    
    window = gui.Window('FloraStudy', layout=layout, margins=(20, 20))
    
    running = True
    
    while running:
        event, values = window.read()
    
    
    return cardSet