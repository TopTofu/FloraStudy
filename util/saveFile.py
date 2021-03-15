import json
from typing import List, Dict

def saveFile(cards: List[Dict[str, str]], filePath: str) -> None:
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cards))
