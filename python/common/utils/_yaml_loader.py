from abc import abstractmethod
import yaml
import os
from typing import TypeVar, Generic
from python.common.utils._custom_logger import LoggingInterface

T = TypeVar("T")


class YAMLFile(LoggingInterface):

    def __init__(self, prefix: str) -> None:
        super().__init__(prefix)

    @abstractmethod
    def _parse_from_data(data: dict) -> None:
        pass


class YAMLLoader(Generic[T]):
    @staticmethod
    def from_file(default: YAMLFile, f: str) -> T:
        # Check if file exist
        if os.path.exists(f):
            with open(f, "r") as config_file:
                try:
                    data = dict(yaml.safe_load(config_file))
                    default._parse_from_data(data)
                    return default
                except yaml.YAMLError as e:
                    LoggingInterface.serror(f'YAML Error when loading "{f}"')
                    return default
        else:
            LoggingInterface.swarn(f'Given config file "{f}" doesn\'t exist')
            return T()
