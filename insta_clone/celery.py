import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta_clone.settings')

app = Celery('insta_clone')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_stories': {
        'task': 'stories.tasks.check_stories_date',
        'schedule': crontab(minute='*/10'),
    },
    'delete_stories': {
        'task': 'stories.tasks.delete_old_stories',
        'schedule': crontab(minute='*/10'),
    }
}