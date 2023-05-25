import boto3

BUCKET_NAME = "blog-tts-pod"

s3_client = boto3.client("s3")
