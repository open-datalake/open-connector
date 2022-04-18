from io import BytesIO
from typing import Iterable
import boto3
from open_connector import DestinationOpenConnector
from open_connector.protocol.pipeline import OpenMessage


class OpenS3Destination(DestinationOpenConnector):

    def __init__(self, config_file: str = 'destination_s3.config.yml'):
        super().__init__(config_file)

        # Create a S3 client
        self.s3 = boto3.client('s3')

    def write(self, messages: Iterable[OpenMessage], **kwargs):

        # Get default values from config
        bucket_name: str = self.config['bucket_name']
        key_prefix: str = self.config.get('key_prefix')
        dataset_name: str = self.config['dataset_name']
        table_name: str = self.config['table_name']
        output_format: str = self.config['output_format']

        # Iterate over each message
        for index, (data, metadata) in enumerate(messages):

            # Get metadata values - override default's ones
            ingestion_time: str = metadata.ingestion_time
            output_format: str = metadata.output_format or output_format

            # Create file path and name
            path_elements = [key_prefix, dataset_name, table_name, f'ingestion_time={ingestion_time}']
            file_path: str = '/'.join(filter(lambda entry: entry, path_elements))
            file_name: str = f"{dataset_name}_{table_name}.{output_format}"

            # Upload to S3
            self.s3.upload_fileobj(
                Fileobj=BytesIO(data),
                Bucket=bucket_name,
                Key=f"{file_path}/{file_name}"
            )
