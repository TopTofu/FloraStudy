from typing import Any, Tuple
from colorama import Fore, Style
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    SUCCESS = Fore.GREEN
    INFO = Fore.CYAN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    
def consoleLog(logLevel: LogLevel, message: str, args: str) -> None:
    if len(args) >= 150:
        args = args[:150] + '...'
        
    print(Fore.BLUE + getTime() + logLevel.value + message + Style.RESET_ALL + args + Style.RESET_ALL)
    
    
def getTime() -> str:
    return f"[{datetime.now().strftime('%H:%M:%S')}] "