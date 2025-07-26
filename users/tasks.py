from celery import shared_task
import time
from datetime import datetime, timedelta
import os

@shared_task
def sent_otp_email(user_email, code):
    print('Sending...')
    time.sleep(20)
    print('Email sent!')

@shared_task
def send_daily_report():
    print('Sending daily report...')
    # Logic to send the daily report
    time.sleep(50)
    print('Daily report sent!')

@shared_task
def cleanup_old_reports():
    folder = "/tmp/"
    cutoff = datetime.now() - timedelta(days=7)
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime < cutoff:
                os.remove(path)
                print(f"Deleted old report {filename}")