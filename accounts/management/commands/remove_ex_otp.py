from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz 
class Command(BaseCommand):
    help = 'remove all expired otp codes'

    def handle(self, *args, **options):
        #return super().handle(*args, **options)
        expired_time = datetime.now(tz=pytz.timezone("UTC")) - timedelta(minutes=1)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('all expired otp code removed')
