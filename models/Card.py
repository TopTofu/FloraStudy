from typing import Dict, Any
from config.Config import Configuration


class Card:
    values: Dict[str, str]
    data: Dict[str, Any]
    mainTerm: str

    def __init__(self, values: Dict[str, str] = {}, mainColumn: str = None, data: Dict[str, Any] = None) -> None:
        self.values = values

        if mainColumn is not None:
            self.mainTerm = self.values[mainColumn]
        elif Configuration.getInstance()._Config.get('mainColumn', None) is not None:
            self.mainTerm = self.values[Configuration.getInstance()._Config['mainColumn']]

        if data is None:
            self.data = {'scoring': 0, 'last studied': None}

    def setMainTerm(self, mainColumn: str) -> None:
        self.mainTerm = self.values[mainColumn]

    def __str__(self) -> str:
        return self.mainTerm

    def update(self, newValues: Dict[str, str], mainColumn: str):
        for key, value in newValues.items():
            self.values.update({key: value})
        
        self.mainTerm = self.values[mainColumn]
