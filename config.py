import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME = "745369-esi3898l-examen1"

DATABASE_URL = os.getenv('DATABASE_URL')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
