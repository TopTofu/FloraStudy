from typing import Dict, List
import PySimpleGUI as gui
from util.saveFile import saveFile


def init(cards: List[Dict[str, str]], config: dict, currentFile: str) -> None:
    layout = [[gui.Input(default_text=currentFile), gui.FileBrowse(key='SAVEPATHINPUT', 
                                           file_types=[('JSON Files', '*.json'),
                                                                            ('FloraStudy Card-Files',
                                                                             config['file-extension'])
                                                                            ])],
              [gui.Button(button_text='Export', key='EXPORT')]]

    window = gui.Window('Export', layout=layout, margins=(20, 20))

    running = True
    while running:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            running = False
        elif event == 'EXPORT':
            filePath = values['SAVEPATHINPUT']
            if values['SAVEPATHINPUT']:
                saveFile(cards, filePath)
            else: 
                saveFile(cards, currentFile)
            window.close()
            