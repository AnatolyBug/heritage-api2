import boto3
from botocore.client import Config
import os


def generate_aws_url(key) -> str:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        config=Config('s3v4'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": os.getenv('AWS_IMAGE_STORAGE_BUCKET_NAME'),
            "Key": key,
            'ResponseContentType': 'image/jpeg'
        },
        ExpiresIn=3600
    )
