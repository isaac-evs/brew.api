import boto3
from botocore.exceptions import ClientError
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL

class SESService:
    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY,
            region_name = AWS_REGION
        )
        self.sender_email = SENDER_EMAIL

    def send_email(self, recipient, subject, body_html, body_text=None):
        if body_text is None:
            body_text = body_html

        try:
            response = self.ses_client.send_email(
                Source = self.sender_email,
                Destination = {
                    'ToAddresses': [recipient],
                },
                Message={
                    'Subject': {
                        'Data': subject,
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text,
                        },
                        'Html': {
                            'Data': body_html,
                        }
                    }
                }
            )
            return response['MessageId']
        except ClientError as e:
            print(f'Error sending email: {e}')
            raise
