import boto3
from open_connector import SourceOpenConnector


class OpenS3Source(SourceOpenConnector):

    def __init__(self, config_file: str = 'source_s3.config.yml'):
        super().__init__(config_file)

        # Create a S3 client
        self.s3 = boto3.client('s3')
