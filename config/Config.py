from types import SimpleNamespace
from typing import Dict
import json
import os


class Configuration:
    
    _Config: Dict[str, str]
    
    _instance = None
    
    @staticmethod
    def getInstance():
        if Configuration._instance == None:
            Configuration()
        return Configuration._instance
    
    def __init__(self) -> None:
        if Configuration._instance is not None:
            raise Exception('Config is a Singleton')
        
        Configuration._instance = self        
    
    
    def loadConfig(self, path: str):
        if os.path.isfile(path):
            with open(path, 'r') as configFile:
                self._Config = json.loads(configFile.read())
