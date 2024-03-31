import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cashback_accrual_every_month_on_the_25th': {
        'task': 'users.tasks.cashback_accrual',
        'schedule': crontab(0, 0, day_of_month='25'),
    },
    'autopay_every_day': {
        'task': 'users.tasks.create_autopay',
        'schedule': crontab(),
    }
}
