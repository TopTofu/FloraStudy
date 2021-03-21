from typing import Dict, List
from util.loadCardSetIntoSettings import loadCardSetIntoSettings
from util.saveFile import saveFile
from models.CardSet import CardSet
import PySimpleGUI as gui
import layout.Layout as Layout


def init(cardSet: CardSet) -> CardSet:

    promptColumns: List[Dict[str, int]] = []
    revealColumns: List[Dict[str, int]] = []

    window = Layout.getStandartWindow(layout=Layout.getSettingsLayout(cardSet))
    window.finalize()

    window, cardSet, promptCount, revealCount, promptSettings, revealSettings = loadCardSetIntoSettings(
        window, cardSet)

    while True:
        event, values = window.read()

        if event == gui.WIN_CLOSED:
            break

        if event in ('PROMPT1', 'PROMPT2', 'PROMPT3', 'PROMPT4'):
            promptSettings.update({event: values[event]})

        if event in ('REVEAL1', 'REVEAL2', 'REVEAL3', 'REVEAL4'):
            revealSettings.update({event: values[event]})

        if event in ('ADDBUTTONPROMPT', 'ADDBUTTONREVEAL'):
            typeToAdd = event[9:]

            if typeToAdd == 'PROMPT':
                count = promptCount
            else:
                count = revealCount

            if count < 4:
                count += 1
                window[f'{typeToAdd}{count}FRAME'].update(visible=True)

                if count == 4:
                    window[f'ADDBUTTON{typeToAdd}'].update(disabled=True)

                window[f'REMOVEBUTTON{typeToAdd}'].update(disabled=False)

            if typeToAdd == 'PROMPT':
                promptCount = count
            else:
                revealCount = count

        if event in ('REMOVEBUTTONPROMPT', 'REMOVEBUTTONREVEAL'):  # remove a row
            typeToRemove = event[12:]  # get type to remove

            if typeToRemove == 'PROMPT':
                count = promptCount
            else:
                count = revealCount  # asign count to the correct typeCount

            if count > 1:  # last row cant be removed
                window[f'{typeToRemove}{count}FRAME'].update(
                    visible=False)  # makes row invisible
                if typeToRemove == 'PROMPT' and f'{typeToRemove}{count}' in promptSettings:
                    # removes the value from the invis row from the prompt dict
                    promptSettings.pop(f'{typeToRemove}{count}')
                elif typeToRemove == 'REVEAL' and f'{typeToRemove}{count}' in revealSettings:
                    revealSettings.pop(f'{typeToRemove}{count}')

                count -= 1  # decrement count

                if count == 1:
                    # disabled the removeButton if there is only one row left
                    window[f'REMOVEBUTTON{typeToRemove}'].update(disabled=True)

                window[f'ADDBUTTON{typeToRemove}'].update(
                    disabled=False)  # enables addButton just in case

            if typeToRemove == 'PROMPT':  # reassign count to the correct typeCount
                promptCount = count
            else:
                revealCount = count

        if event == 'Save':
            for key, value in promptSettings.items():  # adds the values from the prompt dict to a prompt list
                promptColumns.append({value: window[f'{key}SIZE'].get()})

            for key, value in revealSettings.items():
                revealColumns.append({value: window[f'{key}SIZE'].get()})

            # promptList is added to cardSetConfig
            cardSet.cardSetConfig['promptColumns'] = promptColumns
            cardSet.cardSetConfig['revealColumns'] = revealColumns

            saveFile(cardSet, cardSet.originPath)
            window.close()
            break

    return cardSet
