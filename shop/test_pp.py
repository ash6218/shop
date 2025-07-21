# test_parspack.py
import boto3
from shop.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url='https://c999265.parspack.net',
)

resp = s3.list_objects_v2(Bucket='mybucket')
print("="*90)
print(resp)
