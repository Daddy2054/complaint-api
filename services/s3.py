# dotenv.load_dotenv()
import os
import boto3


aws_key = os.getenv("AWS_ACCESS_KEY")
aws_secret = os.getenv("AWS_SECRET")
aws_bucket = os.getenv("AWS_BUCKET")


class S3Service:
    def __init__(self):
        self.key = aws_key
        self.secret = aws_secret
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.bucket = aws_bucket

    def upload(self, path, key, ext):
        self.s3.upload_photo(
            path,
            self.bucket,
            key,
            extra_args={"ACL": "public-read", "ContentType": f"image/{ext}"},
        )
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"
