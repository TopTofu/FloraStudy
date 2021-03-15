from models.CardSet import CardSet
import os
from typing import List, Set, Sized
from util.loadFile import loadFile
from util.saveFile import saveFile
from . import exportToFileWindow
import PySimpleGUI as gui
from util.findCardByKanji import findCardByKanji


def init(config: dict) -> gui.Window:
    gui.theme("DarkTeal2")

    importLayout = [[gui.Text('Choose file to import: '),
                     gui.Input(key='IMPORT', enable_events=True),
                     gui.FileBrowse(key='FILEIMPORT',
                                    target='IMPORT',
                                    file_types=[('ALL Files', '*.*'),
                                                ('FloraStudy Card-Files',
                                                 config['file-extension']),
                                                ('JSON Files', '*.json'),
                                                ('CSV Files', '*.csv')])
                     ]]
    
    menuLayout = [['File', ['Open...::OPEN']]]

    editLayout = [
        [gui.Text('CardName', size=(10, 1)), gui.Input(
            size=(50, 1), key='CARDNAMEINPUT')],
        [gui.Text('Readings', size=(10, 1)), gui.Input(
            size=(50, 1), key='READINGSINPUT')],
        [gui.Text('Meanings', size=(10, 1)), gui.Input(
            size=(50, 1), key='MEANINGSINPUT')],
        [gui.Text('Info', size=(10, 1)), gui.Input(
            size=(50, 1), key='INFOINPUT')],
        [gui.Text('Category', size=(10, 1)), gui.Input(
            size=(50, 1), key='CATEGORYINPUT')],
        [gui.Button('Save', disabled=True, key='SAVEBUTTON'),
         gui.Button('Export', disabled=True, key='EXPORTBUTTON')]]

    layout = [
        [gui.Menu(menuLayout)],
        [gui.Frame('Import', importLayout)],
        [gui.Text(key='FILENAMETEXT',
                  auto_size_text=True, size=(30, 1))],
        [gui.Listbox(values=[], key='CARDLIST',
                     auto_size_text=True, size=(10, 10),
                     enable_events=True),
         gui.Frame('Editor', editLayout)
         ]
    ]
    window = gui.Window(title='FloraStudy', layout=layout, margins=(50, 50))
    return window


def runEventLoop(window: gui.Window, config: dict) -> None:
    running = True
    currentCard = {}
    cardIndex = 0
    cardSet = None  # !!!
    columns = []

    while running:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            running = False
            break

        elif event == 'IMPORT':
            importPath = values['FILEIMPORT']
            if importPath:
                cardSet = CardSet(filePath=importPath)
                # gets the main column from every card to display in listbox
                window['CARDLIST'].update(
                    values=[card[cardSet.mainColumn] for card in cardSet.cards])
                window['FILENAMETEXT'].update(
                    f'{os.path.basename(importPath)}')
                window['EXPORTBUTTON'].update(disabled=False)

        elif event == 'CARDLIST':
            if values['CARDLIST']:
                currentCard, cardIndex = findCardByKanji(
                    values['CARDLIST'][0], cardSet.cards, cardSet.mainColumn)
                columns = cardSet.columns
                window['CARDNAMEINPUT'].update(currentCard[columns[0]])
                window['READINGSINPUT'].update(currentCard[columns[1]])
                window['MEANINGSINPUT'].update(currentCard[columns[2]])
                window['INFOINPUT'].update(currentCard[columns[3]])
                window['CATEGORYINPUT'].update(currentCard[columns[4]])
                window['SAVEBUTTON'].update(disabled=False)

        elif event == 'EXPORTBUTTON':
            exportToFileWindow.init(
                cards=cardSet.cards, config=config, currentFile=values['FILEIMPORT'])

        elif event == 'SAVEBUTTON':
            currentCard.update({
                columns[0]: window['CARDNAMEINPUT'].get(),
                columns[1]: window['READINGSINPUT'].get(),
                columns[2]: window['MEANINGSINPUT'].get(),
                columns[3]: window['INFOINPUT'].get(),
                columns[4]: window['CATEGORYINPUT'].get(),
            })
            cardSet.cards[cardIndex] = currentCard
            window['CARDLIST'].update(
                values=[card[cardSet.mainColumn] for card in cardSet.cards])
