from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable
import yaml
from . import config
from .protocol.pipeline import OpenMessage


class OpenConnector:

    def __init__(self, config_file: str):
        self.config: Dict[str, Any] = self._load_config(
            file_path=f"{config.config_folder}/{config_file}"
        )

    @staticmethod
    def _load_config(file_path: str) -> Dict[str, Any]:
        with open(file_path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)


class SourceOpenConnector(ABC, OpenConnector):

    @abstractmethod
    def read(self, *args, **kwargs) -> Iterable[OpenMessage]:
        """Produce a stream of OpenMessage"""
        pass


class DestinationOpenConnector(ABC, OpenConnector):

    @abstractmethod
    def write(self, messages: Iterable[OpenMessage], *args, **kwargs):
        """Write the content of the given iterable to the destination."""
        pass
