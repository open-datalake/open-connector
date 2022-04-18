from dataclasses import dataclass
from typing import Any, Tuple, Optional


@dataclass
class Metadata:
    ingestion_time: str
    output_format: Optional[str] = None


@dataclass
class OpenMessage:
    data: Any
    metadata: Optional[Metadata] = None

    def __post_init__(self):
        # Iterable configuration
        self._iter_index: int = -1
        self._iterables: Tuple[Any, Metadata] = (self.data, self.metadata)

    def __iter__(self):
        """Allow this class to be unpacked and used as iterable."""
        return self

    def __next__(self):
        """Return the iterables elements: data and metadata."""
        # Iter over the iterables
        self._iter_index += 1
        try:
            return self._iterables[self._iter_index]

        # Stop and reset the iteration
        except IndexError as error:
            self._iter_index = -1
            raise StopIteration
