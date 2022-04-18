import json
from typing import Dict, List
from ..protocol.s3 import S3Object


class EmailsS3SNSEvent:
    """
    New emails on S3 from SNS event.
    This class is an iterator of all newly added objects on S3.
    """

    def __init__(self, event: dict):
        self._iter_index: int = -1  # Event iterator index
        self._events: List[dict] = event['Records']

    @staticmethod
    def _create_structured_event(event_message: str) -> S3Object:
        """Return a S3Object from a raw S3 event message."""
        # Transform string to dict and get S3 action
        message: dict = json.loads(event_message)
        s3_action: Dict[str, str] = message['receipt']['action']

        # Return a S3Object
        return S3Object(
            bucket=s3_action['bucketName'],
            key=s3_action['objectKey']
        )

    def __iter__(self):
        """Allow this class to be used as an iterable events."""
        return self

    def __next__(self) -> S3Object:
        """Return structured events"""

        # Get each raw event
        self._iter_index += 1
        try:
            raw_event: dict = self._events[self._iter_index]

        # Stop and reset the iteration
        except IndexError as error:
            self._iter_index = -1
            raise StopIteration

        # Create and return a S3Object as structured event
        event_message: str = raw_event['Sns']['Message']
        return self._create_structured_event(event_message)
