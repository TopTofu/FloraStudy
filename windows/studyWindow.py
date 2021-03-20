from util.evalutateScore import evaluateScore
import PySimpleGUI as gui
from models.CardSet import CardSet
from models.Card import Card
import layout.Layout as Layout
import random
from config.Config import Configuration
from typing import List
from util.saveFile import saveFile

def init(cardSet: CardSet) -> CardSet:
    
    cardsForReview: List[Card] = cardSet.cards
    
    cardsForReview.sort(key=lambda c: c.data['score'])
    
    firstCard = cardsForReview.pop(0)
    
    difficultyButtons = [[gui.Button(button_text='Easy',
                                     key='EASYBUTTON'),
                          gui.Button(button_text='Medium',
                                     key='MEDIUMBUTTON'),
                          gui.Button(button_text='Hard',
                                     key='HARDBUTTON')]]

    promptLayout = [[gui.Text(firstCard.mainTerm, font=(Configuration.getInstance()._Config['font'], 45), key='PROMPTTEXT', size=(30, 1), justification='center')],
                    [gui.Text(text=firstCard.values[cardSet.columns[1]],
                              font=(
                                  Configuration.getInstance()._Config['font'], 15),
                              key='PROMPTTEXT2', size=(30, 1),
                              justification='center')]]

    revealLayout = [[gui.Button(button_text='Show', key='SHOWBUTTON'),
                     gui.Text(text='', visible=False,
                              key='REVEALFIELD', size=(100, 1),
                              justification='center')]]

    layout = [[gui.Frame(title='', border_width=0, layout=promptLayout, element_justification='center')],
              [gui.HorizontalSeparator()],
              [gui.Frame(title='', border_width=0, layout=revealLayout)],
              [gui.Frame(title='', border_width=0, pad=((0, 0), (70, 70)),
                         layout=[[]])],
              [gui.Frame(title='', layout=difficultyButtons, border_width=0,
                         element_justification='right', visible=False, key='DIFFICULTYBUTTON')]
              ]

    window = Layout.getStandartWindow(layout=layout)
    window.ElementJustification = 'center'

    currentCard = firstCard

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

        if event in ('SHOWBUTTON', ' '):
            window['DIFFICULTYBUTTON'].update(visible=True)
            window['SHOWBUTTON'].update(visible=False)

            window['REVEALFIELD'].update(
                visible=True, value=currentCard.values[cardSet.columns[2]])

            event, values = window.read()

            if event in ('EASYBUTTON', 'MEDIUMBUTTON', 'HARDBUTTON', '1', '2', '3'):
                currentCard.data['score'] = evaluateScore(currentCard, event)
                cardSet.updateCardData(currentCard.data, currentCard)
                
                saveFile(cardSet, cardSet.originPath)
                
                if cardsForReview:
                    currentCard = cardsForReview.pop(0)
                    
                    window['REVEALFIELD'].update(visible=False)
                    window['PROMPTTEXT'].update(currentCard.mainTerm)
                    window['PROMPTTEXT2'].update(currentCard.values[cardSet.columns[1]])
                    window['DIFFICULTYBUTTON'].update(visible=False)
                    window['SHOWBUTTON'].update(visible=True)
                
                else:
                    break

    return cardSet
