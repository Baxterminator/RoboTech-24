from abc import abstractmethod
import yaml
import os
from typing import TypeVar, Generic
from dataclasses import asdict
from ._custom_logger import LoggingInterface

T = TypeVar("T")


class YAMLFile(LoggingInterface):

    def __init__(self, prefix: str) -> None:
        super().__init__(prefix)
        self.file = ""

    @abstractmethod
    def _parse_from_data(data: dict) -> None:
        pass

    @abstractmethod
    def to_yaml(self) -> dict:
        pass

    def export(self) -> None:
        with open(self.file, "w") as calib_file:
            yaml.dump(self.to_yaml(), calib_file)


class YAMLLoader(Generic[T]):
    @staticmethod
    def from_file(default: YAMLFile, f: str) -> T:
        # Check if file exist
        if os.path.exists(f):
            with open(f, "r") as config_file:
                try:
                    data = dict(yaml.safe_load(config_file))
                    default._parse_from_data(data)
                    default.file = f
                    return default
                except yaml.YAMLError as e:
                    LoggingInterface.serror(f'YAML Error when loading "{f}"')
                    return default
        else:
            LoggingInterface.swarn(f'Given config file "{f}" doesn\'t exist')
            return T()
