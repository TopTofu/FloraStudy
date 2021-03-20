import PySimpleGUI as gui
import os
from models.CardSet import CardSet
from models.Card import Card
from util.saveFile import saveFile
from util.findCardByMainColumn import findCardByMainColumn
import layout.Layout as Layout
from . import studyWindow
from windows import cardSetSettingsWindow


def init(cardSet: CardSet) -> None:

    currentCard: Card = Card()
    columns = cardSet.columns

    window = Layout.getMainWindow(cardSet)
    window.ElementJustification = 'center'

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

        elif event == 'Open...':
            importPath = gui.popup_get_file(
                'Open file', no_window=True, file_types=Layout.fileTypes)
            if importPath:
                cardSet = CardSet(filePath=importPath)
                # gets the main column from every card to display in listbox
                window['CARDLIST'].update(values=cardSet.cards)
                window.set_title(
                    f'FloraStudy - {os.path.basename(importPath)}')

        elif event == 'CARDLIST':
            if values['CARDLIST']:
                currentCard = values['CARDLIST'][0]

                columns = cardSet.columns

                for i, column in enumerate(columns):
                    window[column.upper()].update(
                        currentCard.values[columns[i]])

                window['SAVEBUTTON'].update(disabled=False)

        elif event == 'Save as...':
            savePath = Layout.getSaveAsWindow()
            if savePath:
                saveFile(cardSet, savePath)

        elif event == 'Save':
            saveFile(cardSet, cardSet.originPath)

        elif event == 'SAVEBUTTON':
            newValues = {column: window[column.upper()].get()
                         for column in columns}

            if currentCard in cardSet.cards:
                cardIndex = cardSet.cards.index(currentCard)

                cardSet.updateCard(newValues, cardIndex)
                window['CARDLIST'].update(values=cardSet.cards)

                saveFile(cardSet, cardSet.originPath)

        elif event == 'STUDYBUTTON':
            studyWindow.init(cardSet)

        elif event == 'CARDSETSETTINGSBUTTON':
            cardSet = cardSetSettingsWindow.init(cardSet)
