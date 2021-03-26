import layout.Layout as Layout
from windows import mainWindow, baseWindow
import PySimpleGUI as gui
from config.Config import Configuration
from typing import Dict
import sys, os

def main():
    # try:
        Configuration.getInstance().loadConfig('config/config.json')
        
        gui.LOOK_AND_FEEL_TABLE['FloraStudyTheme'] = Layout.theme
        gui.theme('FloraStudyTheme')

        importedCards = baseWindow.init()

        if importedCards is not None:
            mainWindow.init(importedCards)
            
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(f'<{e}> in [{fname}:{exc_tb.tb_lineno}]')

if __name__ == '__main__':
    main()
