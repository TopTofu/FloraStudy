from models.CardSet import CardSet
from typing import Dict
import PySimpleGUI as gui


def loadCardSetIntoSettings(window: gui.Window, cardSet: CardSet):
    promptSettings: Dict[str, str] = {}
    revealSettings: Dict[str, str] = {}

    promptCount: int = 0
    revealCount: int = 0

    for i in (2, 3, 4):
        window[f'PROMPT{i}FRAME'].update(visible=False)
        window[f'REVEAL{i}FRAME'].update(visible=False)

    for i, prompt in enumerate(cardSet.cardSetConfig['promptColumns']):
        promptCount += 1
        window[f'PROMPT{i+1}FRAME'].update(visible=True)
        window[f'PROMPT{i+1}'].update(value=list(prompt.keys())[0])
        window[f'PROMPT{i+1}SIZE'].update(value=list(prompt.values())[0])
        promptSettings.update({f'PROMPT{i+1}': list(prompt.keys())[0]})

    for i, reveal in enumerate(cardSet.cardSetConfig['revealColumns']):
        revealCount += 1
        window[f'REVEAL{i+1}FRAME'].update(visible=True)
        window[f'REVEAL{i+1}'].update(value=list(reveal.keys())[0])
        window[f'REVEAL{i+1}SIZE'].update(value=list(reveal.values())[0])
        revealSettings.update({f'REVEAL{i+1}':list(reveal.keys())[0]})

    if revealCount > 1:
        window['REMOVEBUTTONREVEAL'].update(disabled=False)

    if promptCount > 1:
        window['REMOVEBUTTONPROMPT'].update(disabled=False)

    if promptCount == 4:
        window['ADDBUTTONPROMPT'].update(disabled=True)

    if revealCount == 4:
        window['ADDBUTTONREVEAL'].update(disabled=True)

    return window, cardSet, promptCount, revealCount, promptSettings, revealSettings
