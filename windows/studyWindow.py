import PySimpleGUI as gui
from models.CardSet import CardSet
import layout.Layout as Layout
import random
from config.Config import Configuration


def init(cardSet: CardSet) -> CardSet:
    firstTerm = random.choice(cardSet.cards).mainTerm

    layout = [[gui.Text(firstTerm, font=(Configuration.getInstance()._Config['font'], 45))],
              [gui.Button(button_text='Easy', key='EASYBUTTON'),
               gui.Button(button_text='Medium', key='MEDIUMBUTTON'),
               gui.Button(button_text='Hard', key='HARDBUTTON')]
              ]

    window = Layout.getStandartWindow(layout=layout)

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

    return cardSet
