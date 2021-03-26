from util.log.log import LogLevel, consoleLog
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

    cardsForReview: List[Card] = cardSet.cards.copy()

    cardsForReview.sort(key=lambda c: c.data['score'])
    firstCard = cardsForReview.pop(0)

    difficultyButtons = [[gui.Button(button_text='Easy',
                                     key='EASYBUTTON'),
                          gui.Button(button_text='Medium',
                                     key='MEDIUMBUTTON'),
                          gui.Button(button_text='Hard',
                                     key='HARDBUTTON')]]

    font = Configuration.getInstance()._Config['font']

    # need to use metadata for storing the corisponding column, because the key must be unique and we need to cover the case of the having the same column twice
    promptLayout = [*[[gui.Text(text=firstCard.values[list(col.keys())[0]], size=(50, 1), font=(font, list(col.values())[0]), justification='center',
                                metadata=list(col.keys())[0])] for col in cardSet.cardSetConfig['promptColumns']]]

    revealLayout = [*[[gui.Text(text='', size=(50, 1), font=(font, list(col.values())[0]), justification='center',
                                metadata=list(col.keys())[0])] for col in cardSet.cardSetConfig['revealColumns']]]

    layout = [[gui.Frame(title='', border_width=0, layout=promptLayout, element_justification='center', key='PROMPTFRAME')],
              [gui.HorizontalSeparator()],
              [gui.Frame(title='', border_width=0, layout=revealLayout, key='REVEALFRAME', element_justification='center')],
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
        consoleLog(LogLevel.INFO, f'Event occured: ', f'{event}')

        if event == gui.WIN_CLOSED:
            break

        if event == ' ':
            window['DIFFICULTYBUTTON'].update(visible=True)

            for element in window['REVEALFRAME'].Rows:
                col = element[0].metadata.lower()
                element[0].update(currentCard.values[col])
                
            window['REVEALFRAME'].update(visible=True)    

            event, values = window.read()

            if event in ('EASYBUTTON', 'MEDIUMBUTTON', 'HARDBUTTON', '1', '2', '3'):
                cardSet.cards[currentCard.data['index']
                              ].data['score'] = evaluateScore(currentCard, event)
                saveFile(cardSet, cardSet.originPath)

                if cardsForReview:
                    currentCard = cardsForReview.pop(0)
                    window['REVEALFRAME'].update(visible=False)
                    for element in window['PROMPTFRAME'].Rows:
                        col = element[0].metadata.lower()
                        element[0].update(currentCard.values[col])

                    window['DIFFICULTYBUTTON'].update(visible=False)

                else:
                    window.close()
                    gui.Popup('Set finished!', keep_on_top=True)
                    break

    return cardSet
