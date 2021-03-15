from util.loadConfig import loadConfig
from gui import mainWindow

def main():
    config = loadConfig("config.json")
    window = mainWindow.init(config)
    mainWindow.runEventLoop(window, config)

if __name__ == '__main__':
    main()
