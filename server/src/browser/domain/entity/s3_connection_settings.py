from dataclasses import dataclass


@dataclass
class S3ConnectionSetting:
    id: str
    region_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str