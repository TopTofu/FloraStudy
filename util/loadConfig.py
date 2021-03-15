import json


def loadConfig(filePath: str) -> dict:
    with open(filePath, 'r') as configFile:
        jsonString = configFile.read()
    
    return json.loads(jsonString)
