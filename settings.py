import os

import boto3


class Settings:
    @staticmethod
    def __get_aws_session():
        AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
        AWS_SECRET = os.getenv("AWS_SECRET")
        AWS_REGION = os.getenv("AWS_REGION")
        aws_session = boto3.Session(aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET, region_name = AWS_REGION)
        return aws_session
    @staticmethod
    def get_aws_s3_client():
        aws_session = Settings.__get_aws_session()
        s3 = aws_session.resource('s3')
        return s3.meta.client