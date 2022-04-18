from dataclasses import dataclass


@dataclass
class S3Object:
    bucket: str
    key: str
