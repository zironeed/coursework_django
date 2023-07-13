from django.core.mail import send_mail
from django.conf import settings

import pytz
from datetime import datetime
import smtplib
import schedule
import time

import mailingapp.models


def sendmail_registration(new_user_email: list, message_title: str, message_body: str):
    send_mail(message_title, message_body, settings.EMAIL_HOST_USER, [new_user_email], fail_silently=True)


def sendmail(mailing_id: str, emails_base: list, message_title: str, message_body: str) -> None:
    try:
        send_mail(message_title, message_body, settings.EMAIL_HOST_USER, emails_base, fail_silently=True)

        statistic = mailingapp.models.Statistic.objects.get(mailing_id=mailing_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "OK"
        statistic.time = datetime.now(pytz.timezone('Europe/Moscow'))
        statistic.save()

        change_mailing_status = mailingapp.models.MailingSettings.objects.get(id=mailing_id)
        change_mailing_status.status = "FINISHED"
        change_mailing_status.save()

        print("SEND MAIL")

    except smtplib.SMTPException as send_error:

        print("PROBLEMS WITH SEND MAIL")
        statistic = mailingapp.models.Statistic.objects.get(mailing_id=mailing_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "ERROR"
        statistic.time = datetime.now(pytz.timezone('Europe/Moscow'))
        statistic.save()

        change_mailing_status = mailingapp.models.MailingSettings.objects.get(id=mailing_id)
        change_mailing_status.status = "FINISHED_WITH_ERROR"
        change_mailing_status.save()


def run_schedule():
    """Work with scheduler"""
    schedule.clear()
    active_mailing = mailingapp.models.MailingSettings.objects.filter(is_published=True)
    print("PREPARE SEND")

    # DAILY SCHEDULER
    for mailing in active_mailing:
        emails_base = []
        print("MAILING TITLE:", mailing.title)

        if mailing.frequency == "DAILY":
            print("TYPE: SEND DAILY")
            print("ID:", mailing.pk)
            convert_time = str(mailing.time)[:5]
            print("TIME:", convert_time)
            message = mailing.get_messages()
            print("MESSAGE TITLE:", message.title)
            print("MESSAGE BODY:", message.body)
            for client_mail in mailing.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                schedule.every().day.at(convert_time).do(sendmail,
                                                         emails_base=emails_base,
                                                         message_title=message.title,
                                                         message_body=message.body,
                                                         mailing_id=mailing.pk
                                                         )
                change_mailing_status = mailingapp.models.MailingSettings.objects.get(id=mailing.pk)
                change_mailing_status.status = "READY"
                change_mailing_status.save()

        today = datetime.today().weekday()
        if mailing.frequency == "WEEKLY":
            print("TYPE: SEND WEEKLY")
            print("ID:", mailing.pk)
            convert_time = str(mailing.time)[:5]
            print("TIME:", convert_time)
            message = mailing.get_messages()
            print("MESSAGE TITLE:", message.title)
            print("MESSAGE BODY:", message.body)
            for client_mail in mailing.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                if today == 0:
                    schedule.every().sunday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_title=message.title, message_body=message.body,
                                                                mailing_id=mailing.pk)
                if today == 1:
                    schedule.every().monday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_title=message.title, message_body=message.body,
                                                                mailing_id=mailing.pk)
                if today == 2:
                    schedule.every().tuesday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                 message_title=message.title, message_body=message.body,
                                                                 mailing_id=mailing.pk)
                if today == 3:
                    schedule.every().wednesday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                   message_title=message.title, message_body=message.body,
                                                                   mailing_id=mailing.pk)
                if today == 4:
                    schedule.every().thursday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                  message_title=message.title, message_body=message.body,
                                                                  mailing_id=mailing.pk)
                if today == 5:
                    schedule.every().friday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_title=message.title, message_body=message.body,
                                                                mailing_id=mailing.pk)
                if today == 6:
                    schedule.every().saturday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                  message_title=message.title, message_body=message.body,
                                                                  mailing_id=mailing.pk)

                change_mailing_status = mailingapp.models.MailingSettings.objects.get(id=mailing.pk)
                change_mailing_status.status = "READY"
                change_mailing_status.save()

        if mailing.frequency == "MONTHLY":
            print("TYPE: SEND MONTHLY")
            print("ID:", mailing.pk)
            convert_time = str(mailing.time)[:5]
            print("TIME:", convert_time)
            message = mailing.get_messages()
            print("MESSAGE TITLE:", message.title)
            print("MESSAGE BODY:", message.body)
            for client_mail in mailing.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)
                schedule.every(4).weeks.do(sendmail, emails_base=emails_base, message_title=message.title,
                                           message_body=message.body, mailing_id=mailing.pk)

                change_mailing_status = mailingapp.models.MailingSettings.objects.get(id=mailing.pk)
                change_mailing_status.status = "READY"
                change_mailing_status.save()

        print("ALL JOBS:")
        print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)
