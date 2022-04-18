from typing import Iterable
from datetime import datetime
from open_connector.events.sns import EmailsS3SNSEvent
from open_connector.protocol.pipeline import OpenMessage, Metadata
from ..source import OpenS3Source


class EmailLandingSource(OpenS3Source):

    def __init__(self, event: dict):
        super().__init__()
        self._event = event

    def read(self) -> Iterable[OpenMessage]:
        """Get the newly added emails. Yield them back as OpenMessages."""

        # Loop over each new emails in the datalake
        for s3_object in EmailsS3SNSEvent(self._event):

            # Get file from S3
            response: dict = self.s3.get_object(
                Bucket=s3_object.bucket,
                Key=s3_object.key
            )

            # Save as bytes
            file_object: bytes = response['Body'].read()

            # Send to the destination
            yield OpenMessage(
                data=file_object,
                metadata=Metadata(
                    ingestion_time=datetime.now().isoformat(),
                    output_format='email'
                )
            )
