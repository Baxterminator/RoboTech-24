from enum import Enum

DEBUG_PREFIX = "[D]"
INFO_PREFIX = "[I]"
WARN_PREFIX = "[W]"
ERROR_PREFIX = "[E]"

try:
    from colorama import Fore, Back, Style

    DEBUG_PREFIX = Fore.GREEN + DEBUG_PREFIX
    INFO_PREFIX = Fore.RESET + INFO_PREFIX
    WARN_PREFIX = Fore.YELLOW + WARN_PREFIX
    ERROR_PREFIX = Fore.RED + ERROR_PREFIX

except ImportError as e:
    pass


class LogLevel(Enum):
    DEBUG = 0
    INFO = 2
    WARN = 4
    ERROR = 6


class LoggingInterface:

    LOGGING_LVL = LogLevel.INFO

    def __init__(self, prefix: str) -> None:
        self.__prefix = prefix

    def __print(self, msg: str, lvl_pref: str, lvl: LogLevel) -> None:
        print(f"{lvl_pref}[{self.__prefix}]{msg}")

    def debug(self, msg: str) -> None:
        self.__print(msg, DEBUG_PREFIX, LogLevel.DEBUG)

    def info(self, msg: str) -> None:
        self.__print(msg, INFO_PREFIX, LogLevel.INFO)

    def warn(self, msg: str) -> None:
        self.__print(msg, WARN_PREFIX, LogLevel.WARN)

    def error(self, msg: str) -> None:
        self.__print(msg, ERROR_PREFIX, LogLevel.ERROR)
