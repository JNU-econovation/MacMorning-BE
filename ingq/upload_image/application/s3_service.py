import boto3

from core.setting.load_env import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_REGION,
    AWS_S3_BUCKET_NAME,
    AWS_SECRET_ACCESS_KEY,
)


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket_name = AWS_S3_BUCKET_NAME

    def generate_presigned_url(
        self, key: str, content_type: str, expires_in: int = 60 * 5
    ) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
