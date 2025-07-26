from celery import shared_task
import time

@shared_task
def sent_otp_email(user_email, code):
    print('Sending...')
    time.sleep(20)
    print('Email sent!')