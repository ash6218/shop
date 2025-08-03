from celery import shared_task
from utils import send_otp_code
from accounts.models import OtpCode
from datetime import datetime, timedelta
from bucket import bucket
import pytz


@shared_task
def send_otp_code_task(phone_number, code):
    send_otp_code(phone_number, code)

@shared_task
def remove_ex_otp():
    expired_time = datetime.now(tz=pytz.timezone("UTC")) - timedelta(minutes=1)
    OtpCode.objects.filter(created__lt=expired_time).delete()

@shared_task
def upload_object_task(name, content):
    bucket.upload_object(name, content) 