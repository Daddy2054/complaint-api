import os
import boto3
from fastapi import HTTPException
import logging
from botocore.exceptions import ClientError
from botocore.config import Config


aws_key = os.getenv("AWS_ACCESS_KEY")
aws_secret = os.getenv("AWS_SECRET")
aws_bucket = os.getenv("AWS_BUCKET")
aws_region = os.getenv("AWS_REGION")

my_config = Config(
    region_name=aws_region,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


class S3Service:
    def __init__(self):
        self.key = aws_key
        self.secret = aws_secret
        self.s3 = boto3.client(
            "s3",
            config=my_config)
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )
        self.bucket = aws_bucket

    def upload(self, path, key, ext):
        try:
            self.s3.upload_file(
                path,
                self.bucket,
                key,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"},
            )
        except Exception as ex:
            raise HTTPException(500, "S3 is not configured correctly")
        except ClientError as e:
            logging.error(e)
            raise HTTPException(500, f"S3 error{e}")

        return f"https://{self.bucket}.s3.{aws_region}.amazonaws.com/{key}"


