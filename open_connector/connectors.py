from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Optional
from datetime import datetime
import logging
import yaml
from . import config
from .protocol.pipeline import OpenMessage, Metadata

# Create logger
logger = logging.getLogger(__name__)


class OpenConnector:

    def __init__(self, config_file: str):
        self.config: Dict[str, Any] = self._load_config(
            file_path=f"{config.config_folder}/{config_file}"
        )

    @staticmethod
    def _load_config(file_path: str) -> Dict[str, Any]:
        """
        Load the connector config file. Return it as dict. Return an empty
        dict if no file is found.
        """
        try:
            with open(file_path) as file:
                return yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError as error:
            logger.warning(
                f"File '{file_path}' not found. Loading default empty config. "
                "This may cause failure during the execution of this connector."
            )
            return {}


class SourceOpenConnector(ABC, OpenConnector):

    @abstractmethod
    def read(self, *args, **kwargs) -> Iterable[OpenMessage]:
        """Produce a stream of OpenMessage"""
        pass

    @staticmethod
    def open_message(
            file_object: bytes,
            output_format: Optional[str] = None
    ) -> OpenMessage:
        """Create and return an OpenMessage object."""

        return OpenMessage(
            data=file_object,
            metadata=Metadata(
                ingestion_time=datetime.now().isoformat(),
                output_format=output_format or "object"
            )
        )


class DestinationOpenConnector(ABC, OpenConnector):

    @abstractmethod
    def write(self, messages: Iterable[OpenMessage], *args, **kwargs):
        """Write the content of the given iterable to the destination."""
        pass
