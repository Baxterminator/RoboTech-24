from enum import IntEnum
from datetime import datetime
from typing import List, Tuple

DEBUG_PREFIX = "[D]"
INFO_PREFIX = "[I]"
WARN_PREFIX = "[W]"
ERROR_PREFIX = "[E]"
SUFFIX = ""

HEADER_CENTER = ""
HEADER_LEFT = ""
HEADER_SEP = ""

HEADER_WIDTH = 100
NAME_WIDTH = 13

try:
    from colorama import Fore, Back, Style

    DEBUG_PREFIX = Fore.GREEN + DEBUG_PREFIX
    INFO_PREFIX = Fore.RESET + INFO_PREFIX
    WARN_PREFIX = Style.DIM + Fore.RED + WARN_PREFIX
    ERROR_PREFIX = Style.DIM + Fore.LIGHTMAGENTA_EX + ERROR_PREFIX
    SUFFIX = Style.RESET_ALL

    HEADER_SEP = Style.BRIGHT + Fore.LIGHTRED_EX
    HEADER_CENTER = Style.BRIGHT + Fore.CYAN
    HEADER_LEFT = Fore.LIGHTBLUE_EX

except ImportError as e:
    print("Colorama not present !")
    pass


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 2
    WARN = 4
    ERROR = 6


class LoggingInterface:

    LOGGING_LVL = LogLevel.INFO

    def __init__(self, prefix: str) -> None:
        self.__prefix = prefix

    # =========================================================================
    #                                  CONFIG
    # =========================================================================
    @staticmethod
    def configure_lvl(level: str) -> None:
        match level:
            case "debug":
                LoggingInterface.LOGGING_LVL = LogLevel.DEBUG
            case "warn":
                LoggingInterface.LOGGING_LVL = LogLevel.WARN
            case "error":
                LoggingInterface.LOGGING_LVL = LogLevel.ERROR
            case _:
                LoggingInterface.LOGGING_LVL = LogLevel.INFO

    # =========================================================================
    #                                 PRINTING
    # =========================================================================

    def __print(self, msg: str, lvl_pref: str, lvl: LogLevel) -> None:
        LoggingInterface.__sprint(msg, lvl_pref, lvl, self.__prefix)

    @staticmethod
    def __sprint(msg: str, lvl_prf: str, lvl: LogLevel, prf: str = "") -> None:
        if lvl >= LoggingInterface.LOGGING_LVL:
            try:
                time = datetime.now().strftime("%H:%M:%S")
            except:
                time = "--------"
            print(
                lvl_prf
                + f"[{time}]"
                + (f"[{prf.center(NAME_WIDTH)}] " if len(prf) > 0 else " ")
                + msg
                + SUFFIX
            )

    def _debug(self, msg: str) -> None:
        self.__print(msg, DEBUG_PREFIX, LogLevel.DEBUG)

    @staticmethod
    def sdebug(msg: str) -> None:
        LoggingInterface.__sprint(msg, DEBUG_PREFIX, LogLevel.DEBUG)

    def _info(self, msg: str) -> None:
        self.__print(msg, INFO_PREFIX, LogLevel.INFO)

    @staticmethod
    def sinfo(msg: str) -> None:
        LoggingInterface.__sprint(msg, INFO_PREFIX, LogLevel.INFO)

    def _warn(self, msg: str) -> None:
        self.__print(msg, WARN_PREFIX, LogLevel.WARN)

    @staticmethod
    def swarn(msg: str) -> None:
        LoggingInterface.__sprint(msg, WARN_PREFIX, LogLevel.WARN)

    def _error(self, msg: str) -> None:
        self.__print(msg, ERROR_PREFIX, LogLevel.ERROR)

    @staticmethod
    def serror(msg: str) -> None:
        LoggingInterface.__sprint(msg, ERROR_PREFIX, LogLevel.ERROR)


def printHeader(text: List[Tuple[str, bool]]) -> None:
    print(HEADER_SEP + "".center(HEADER_WIDTH, "=") + SUFFIX)
    for line in text:
        if line[1]:
            print(HEADER_LEFT + line[0].ljust(HEADER_WIDTH) + SUFFIX)
        else:
            print(HEADER_CENTER + line[0].center(HEADER_WIDTH) + SUFFIX)
    print(HEADER_SEP + "".center(HEADER_WIDTH, "=") + SUFFIX)


def printSection(text: str) -> None:
    print(HEADER_SEP + f" {text} ".center(HEADER_WIDTH, "=") + SUFFIX)
