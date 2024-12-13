import os
import boto3
from fastapi import HTTPException
from botocore.exceptions import ClientError
from botocore.config import Config


aws_key = os.getenv("AWS_ACCESS_KEY")
aws_secret = os.getenv("AWS_SECRET")
aws_region = os.getenv("AWS_REGION")
ses_from_mail = os.getenv("AWS_SES_FROM_MAIL")
ses_to_mail = os.getenv("AWS_SES_TO_MAIL")

class SESService:
    def __init__(self):
        self.key = aws_key
        self.secret = aws_secret
        
        self.ses = boto3.client(
            "ses",
            region_name=aws_region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
        )

    def send_mail(self, subject, to_addresses, text_data):

        try:
            response = self.ses.send_email(
                Source=ses_from_mail,
                Destination={"ToAddresses": [ses_to_mail],
                             "CcAddresses": [],
                             "BccAddresses": []},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Text": {"Data": text_data, "Charset": "UTF-8"}},
                },
            )
            # print(response)
        except ClientError as e:
            raise HTTPException(500, f"SES error{e}")