import os
from util.loadFile import loadFile
class CardSet:
    
    def __init__(self, filePath: str) -> None:
        self.originPath = filePath
        
        if os.path.isfile(filePath):
            self.cards, self.columns = loadFile(filePath=filePath)
            self.mainColumn = self.columns[0]