import os

from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_daily_report': {
        'task': 'users.tasks.send_daily_report',
        'schedule': crontab(hour=0, minute=0)
    },
}
