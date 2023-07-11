from django.core.mail import send_mail
from django.conf import settings
import datetime
from datetime import date


def sendmail(to, subject, message):
    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              [to],
              fail_silently=False)


time_now = datetime.datetime.now().isoformat()
print(time_now)
