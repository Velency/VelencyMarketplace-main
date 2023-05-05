import boto3
from django.conf import settings
from botocore.client import Config

def upload_to_s3(local_file, s3_file):
    s3 = boto3.client("s3",
                      region_name=settings.AWS_REGION_NAME,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      config=Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION))
    s3.upload_file(local_file, settings.AWS_STORAGE_BUCKET_NAME, s3_file)


def download_from_s3(s3_file, local_file):
    s3 = boto3.client("s3",
                      region_name=settings.AWS_REGION_NAME,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      config=Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION))
    s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, s3_file, local_file)