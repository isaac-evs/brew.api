import boto3
from botocore.exceptions import ClientError
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET_NAME

class S3Service:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY,
            region_name = AWS_REGION
        )
        self.bucket_name = S3_BUCKET_NAME

    def upload_file(self, file_data, file_name):
        try:
            self.s3_client.put_object(
                Bucket = self.bucket_name,
                Key=file_name,
                Body=file_data,
                Metadata={
                    'read-by-mail': 'false'
                }
            )
            return f'https://{self.bucket_name}.s3.amazonaws.com/{file_name}'

        except ClientError as e:
            print(f'Error uploading file: {e}')
            raise

    def get_file(self, file_name):
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return response['Body'].read()

        except ClientError as e:
            print(f'Error getting file: {e}')
            raise


    def update_metadata(self, file_name):
        try:
            copy_source = {'Bucket': self.bucket_name, 'Key': file_name}

            response = self.s3_client.head_object(
                Bucket = self.bucket_name,
                Key = file_name
            )
            metadata = response.get('Metadata', {})

            metadata['read-by-mail'] = 'true'

            self.s3_client.copy_object(
                Bucket = self.bucket_name,
                Key = file_name,
                CopySource = copy_source,
                Metadata = metadata,
                MetadataDirective = 'REPLACE'
            )
            return True
        except ClientError as e:
            print(f'Error updating metadata: {e}')
            raise
