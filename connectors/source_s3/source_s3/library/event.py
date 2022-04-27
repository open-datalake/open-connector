from typing import Iterable
from open_connector.events.sns import EmailsS3SNSEvent
from open_connector.protocol.pipeline import OpenMessage
from source_s3 import OpenS3Source


class IterableSource(OpenS3Source):

    def __init__(self, iterable_reader: Iterable, output_format: str):
        super().__init__()
        self._iterable_reader: Iterable = iterable_reader
        self._output_format: str = output_format

    def read(self) -> Iterable[OpenMessage]:
        """Get the file from an iterable. Yield them back as OpenMessages."""

        # Loop over each new S3 Object in the iterable
        for s3_object in self._iterable_reader:

            # Get the corresponding file from S3
            response: dict = self.s3.get_object(
                Bucket=s3_object.bucket,
                Key=s3_object.key
            )

            # Load as bytes
            file_object: bytes = response['Body'].read()

            # Send to the destination
            yield self.open_message(
                file_object,
                output_format=self._output_format
            )
