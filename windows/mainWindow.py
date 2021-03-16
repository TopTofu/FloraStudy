import PySimpleGUI as gui
import os
from models.CardSet import CardSet
from typing import Dict, Union
from util.saveFile import saveFile
from util.findCardByMainColumn import findCardByMainColumn
import layout.Layout as Layout


def init(cardSet: CardSet, config: Dict[str, str]) -> None:

    currentCard: Union[Dict[str, str], None] = None
    currentCardIndex: Union[int] = -1
    columns = cardSet.columns

    window = Layout.getMainWindow(cardSet)

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
                window['CARDLIST'].update(values=cardSet.listValues)
                window.set_title(
                    f'FloraStudy - {os.path.basename(importPath)}')

        elif event == 'CARDLIST':
            if values['CARDLIST']:
                currentCard, currentCardIndex = findCardByMainColumn(
                    values['CARDLIST'][0], cardSet)
                columns = cardSet.columns

                for i, column in enumerate(columns):
                    window[column.upper()].update(currentCard[columns[i]])

                window['SAVEBUTTON'].update(disabled=False)

        elif event == 'Save as...':
            savePath = gui.popup_get_file(
                'Save File', no_window=True, file_types=Layout.fileTypes, save_as=True)
            saveFile(cardSet.cards, savePath)

        elif event == 'Save':
            saveFile(cardSet.cards, cardSet.originPath)

        elif event == 'SAVEBUTTON':
            newCard = {}
            
            for i, column in enumerate(columns):
                newCard.update({
                    column: window[column.upper()].get()
                })
                
            cardSet.updateCard(newCard, currentCardIndex)
            window['CARDLIST'].update(values=cardSet.listValues)
