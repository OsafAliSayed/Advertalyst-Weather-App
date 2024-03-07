from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

app = Celery('weather')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# scedule tasks here 
from celery.schedules import crontab

app.conf.beat_schedule = {
    'update-weather-every-hour': {
        'task': 'api.tasks.update_weather',
        'schedule': crontab(minute=0),  # Execute every hour
    },
}