from random import vonmisesvariate
from types import BuiltinFunctionType
from typing import Dict, Text
from models.CardSet import CardSet
import PySimpleGUI as gui
import layout.Layout as Layout


def init(cardSet: CardSet) -> CardSet:

    promptSettings: Dict[str, str] = {}
    reavealSettings: Dict[str, str] = {}

    promptSettingsLayout = [[gui.Frame(title='', border_width=0,
                                       layout=Layout.getChoiceLayoutFirst(cardSet=cardSet))],
                            [gui.Frame(title='', border_width=0,
                                       layout=Layout.getChoiceLayout(
                                           key='PROMPT2', values=cardSet.columns),
                                       visible=False, key='PROMPTFRAME2')],
                            [gui.Frame(title='', border_width=0,
                                       layout=Layout.getChoiceLayout(
                                           key='PROMPT3', values=cardSet.columns),
                                       visible=False, key='PROMPTFRAME3')]]

    revealSettingsLayout = [[]]

    layout = [[gui.Frame(title='Prompt', layout=promptSettingsLayout, key='PROMPTFRAME')],
              [gui.Frame(title='Reveal', layout=revealSettingsLayout)]]

    window = Layout.getStandartWindow(layout=layout)
    

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break
        
        

        if event in ('PROMPT1', 'PROMPT2', 'PROMPT3'):
            promptSettings.update({event: values[event]})

    return cardSet
