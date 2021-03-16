import PySimpleGUI as gui
from models.CardSet import CardSet
from typing import Union
import layout.Layout as Layout

fileTypes = (('ALL Files', '*.*'),
             ('FloraStudy Card-Files', '*.fsc'),
             ('JSON Files', '*.json'),
             ('CSV Files', '*.csv'))


def init() -> Union[CardSet, None]:
    layout = [[gui.Menu(menu_definition=Layout.getMenuLayout(),
                        background_color='#FFFFFF')]]

    window = Layout.getStandartWindow(layout=layout)
    
    cards : Union[CardSet, None] = None

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

        if event == 'Open...':
            importPath = gui.popup_get_file(
                'Open file', no_window=True, file_types=fileTypes)
            if importPath:
                cards = CardSet(importPath)
                break
    
    window.close()
    return cards
