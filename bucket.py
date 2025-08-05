import boto3
import boto3.session
from django.conf import settings
from io import BytesIO

class Bucket:
    """CDN Bucket manager

    init method creates connection.
    
    Note: None of these methods are Async

    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None
        
    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True
    
    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self, name, content):
        self.conn.upload_fileobj(BytesIO(content), settings.AWS_STORAGE_BUCKET_NAME, name)

bucket = Bucket()

def list_s3_images():
    session = boto3.session.Session()
    s3 = session.client(
        service_name=settings.AWS_SERVICE_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    )
    response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    images1, images2 = [], []
    for obj in response.get('Contents', []):
        key = obj['Key']
        size = obj['Size']
        if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"
            images1.append((url, key))  # (value, label)
            images2.append({'url':url, 'key':key, 'size':size})
    return images1, images2