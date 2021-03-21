from windows.cardSetSettingsWindow import init
from config.Config import Configuration
from models.CardSet import CardSet
import PySimpleGUI as gui
from typing import KeysView, List, Sized, Union
import os

fileTypes = (('ALL Files', '*.*'),
             ('FloraStudy Card-Files', '*.fsc'),
             ('JSON Files', '*.json'),
             ('CSV Files', '*.csv'))

fileSaveTypes = (('JSON Files', '*.json'),
                 ('FloraStudy Card-Files', '*.fsc'))

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


def getMenuLayout() -> List[List[Union[str, List[str]]]]:
    return [['File', ['Open...', 'Save', 'Save as...']]]


def getStandartWindow(layout: List[List[gui.Element]], title: str = 'FloraStudy') -> gui.Window:
    return gui.Window(title=title, layout=layout, size=(500, 400), return_keyboard_events=True, use_default_focus=False)


def getMainWindow(cardSet: CardSet) -> gui.Window:
    editorLayout = createEditorLayout(cardSet.columns)

    layout = [
        [gui.Menu(getMenuLayout(), background_color='#FFFFFF')],
        [gui.Listbox(values=cardSet.cards, key='CARDLIST', auto_size_text=False,
                     size=(10, 13), enable_events=True, select_mode=gui.LISTBOX_SELECT_MODE_SINGLE,
                     no_scrollbar=False, font=(Configuration.getInstance()._Config.get('font'), 11)),
         gui.Frame('Edit', editorLayout)],
        [gui.Button(button_text='Study', key='STUDYBUTTON')]
    ]

    return getStandartWindow(layout=layout, title=f'FloraStudy - {os.path.basename(cardSet.originPath)}')


def getSaveAsWindow():
    return gui.popup_get_file('Save File', no_window=True, file_types=fileSaveTypes, save_as=True)


def getSettingsFrameLayout(cardSet: CardSet, kind: str, rows: int) -> List[List[gui.Element]]:
    return [[gui.Frame(title='', border_width=0,
                       layout=[[gui.Combo(values=cardSet.columns,
                                          enable_events=True, key=f'{kind}1',
                                          readonly=True),
                                gui.Spin(values=list(range(5, 60)),
                                         initial_value=12, enable_events=True,
                                         key=f'{kind}1SIZE', readonly=True)]],
                       key=f'{kind}1FRAME'),
             gui.Button('+', key=f'ADDBUTTON{kind}',
                        size=(1, 1), auto_size_button=False),
             gui.Button('-', key=f'REMOVEBUTTON{kind}',
                        size=(1, 1), auto_size_button=False, disabled=True)],
            *[getOptionFrame(kind, cardSet, i) for i in range(2, rows+2)]]


def getOptionFrame(kind: str, cardSet: CardSet, index: int):
    return [gui.Frame(title='', border_width=0,
                      layout=[[gui.Combo(values=cardSet.columns,
                                         enable_events=True,
                                         readonly=True,
                                         key=f'{kind}{index}'),
                               gui.Spin(values=list(range(5, 60)),
                                        initial_value=12, enable_events=True,
                                        key=f'{kind}{index}SIZE', readonly=True)]],
                      key=f'{kind}{index}FRAME')]


def getSettingsLayout(cardSet: CardSet):
    return [[gui.Frame(title='Prompt', layout=getSettingsFrameLayout(cardSet, 'PROMPT', 3),
                       key='PROMPTSETTINGSFRAME')],
            [gui.Frame(title='Reveal', layout=getSettingsFrameLayout(cardSet, 'REVEAL', 3),
                       key='REVEALSETTINGSFRAME')],
            [gui.Button(button_text='Save')]]


def createEditorLayout(columns: List[str]) -> List[List[gui.Element]]:
    layout = []

    for column in columns:
        section = [gui.Text(column.capitalize(), size=(15, 1)),
                   gui.Input(size=(50, 1), key=column.upper(), font=(Configuration.getInstance()._Config['font'], 11))]
        layout.append(section)

    layout.extend([[
        gui.Frame(title='', border_width=0, element_justification='left',
                  layout=[[gui.Button('Save', key='SAVEBUTTON')]]),
        gui.Frame(title='', border_width=0, element_justification='right',
                  layout=[[gui.Button('Set Settings', key='CARDSETSETTINGSBUTTON')]], pad=((200, 0), (0, 0)))
    ]])

    return layout
