import layout.Layout as Layout
from windows import mainWindow, baseWindow
import PySimpleGUI as gui
from config.Config import Configuration
from typing import Dict

def main():
    Configuration.getInstance().loadConfig('config/config.json')
    
    gui.LOOK_AND_FEEL_TABLE['FloraStudyTheme'] = Layout.theme
    gui.theme('FloraStudyTheme')

    importedCards = baseWindow.init()

    if importedCards is not None:
        mainWindow.init(importedCards)


if __name__ == '__main__':
    main()
