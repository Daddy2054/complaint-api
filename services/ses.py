import os
import boto3
from fastapi import HTTPException
#import logging
from botocore.exceptions import ClientError
from botocore.config import Config


aws_key = os.getenv("AWS_ACCESS_KEY")
aws_secret = os.getenv("AWS_SECRET")
aws_region = os.getenv("AWS_REGION")
ses_mail = os.getenv("SES_MAIL")

class S3Service:
    def __init__(self):
        self.key = aws_key
        self.secret = aws_secret
        
        self.s3 = boto3.client(
            "ses",
            region_name=aws_region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )

    def send_mail(self, subject, to_addresses, text_data):

        body =  {"Text": {"Data": text_data, "Charset": "UTF-8"}}
        try:
            self.ses.send_email(
                Source=ses_mail,
                Destination={"ToAddresses": to_addresses,
                             "CcAddresses": [],
                             "BccAddresses": []},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Text": {"Data": body}},
                },
            )
        except ClientError as e:
            raise HTTPException(500, f"SES error{e}")