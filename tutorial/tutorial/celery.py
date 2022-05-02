import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')

app = Celery('app', broker='amqp://guest:guest@rabbitmq:5672//')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule ={
    'notify-user-every-day':{
        'task': 'movie_auth.tasks.notify_user',
        'schedule': crontab(minute=0, hour=12)
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')