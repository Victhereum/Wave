import boto3
from django.conf import settings

from wave.utils.settings import get_app_settings

access_key = settings.AWS_ACCESS_KEY_ID
secret = settings.AWS_SECRET_ACCESS_KEY
bucket = settings.AWS_STORAGE_BUCKET_NAME
enpoint_url = settings.AWS_S3_ENDPOINT_URL

if "production" in get_app_settings():
    region = settings.AWS_S3_REGION_NAME
else:
    region = None

options = {
    "endpoint_url": enpoint_url,
    "aws_access_key_id": access_key,
    "aws_secret_access_key": secret,
    "region_name": region,
}

s3_client = boto3.client("s3", **options)
