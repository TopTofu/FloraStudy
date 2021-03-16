from models.CardSet import CardSet
import PySimpleGUI as gui
from typing import List, Union
import os

fileTypes = (('ALL Files', '*.*'),
             ('FloraStudy Card-Files', '*.fsc'),
             ('JSON Files', '*.json'),
             ('CSV Files', '*.csv'))

theme = {
    'BACKGROUND': '#7B92A8',
    'TEXT': '#000000',
    'INPUT': '#AFBDCA',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#AFBDCA',
    'BUTTON': ('#DFE3EE', '#567857'),
    'PROGRESS':  ('#D1826B', '#CC8019'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}


def createEditorLayout(columns: List[str]) -> List[List[gui.Element]]:
    layout = []

    for column in columns:
        section = [gui.Text(column.capitalize(), size=(15, 1)),
                   gui.Input(size=(50, 1), key=column.upper())]
        layout.append(section)

    layout.append([gui.Button('Save', key='SAVEBUTTON')])

    return layout


def getMenuLayout() -> List[List[Union[str, List[str]]]]:
    return [['File', ['Open...', 'Save', 'Save as...']]]


def getStandartWindow(layout: List[List[gui.Element]], title: str = 'FloraStudy') -> gui.Window:
    return gui.Window(title=title, layout=layout, size=(500, 400))


def getMainWindow(cards: CardSet) -> gui.Window:
    editorLayout = createEditorLayout(cards.columns)

    layout = [
        [gui.Menu(getMenuLayout(), background_color='#FFFFFF')],
        [gui.Listbox(values=cards.listValues, key='CARDLIST', auto_size_text=False,
                     size=(10, 13), enable_events=True, select_mode=gui.LISTBOX_SELECT_MODE_SINGLE, 
                     no_scrollbar=False),
         gui.Frame('Edit', editorLayout)],
        [gui.Button(button_text='Study')]
    ]

    return getStandartWindow(layout=layout, title=f'FloraStudy - {os.path.basename(cards.originPath)}')
