import layout.Layout as Layout
from util.loadConfig import loadConfig
from windows import mainWindow, baseWindow
import PySimpleGUI as gui


def main():
    config = loadConfig("config.json")
    
    gui.LOOK_AND_FEEL_TABLE['FloraStudyTheme'] = Layout.theme
    
    gui.theme('FloraStudyTheme')
    
    importedCards = baseWindow.init()
    
    if importedCards is not None:
        mainWindow.init(importedCards, config)

if __name__ == '__main__':
    main()
