from __future__ import absolute_import, unicode_literals
import os 
from datetime import timedelta
from celery import Celery 
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shuddhi.settings') 
  
app = Celery('shuddhi') 
  
# Using a string here means the worker doesn't  
# have to serialize the configuration object to  
# child processes. - namespace='CELERY' means all  
# celery-related configuration keys should  
# have a `CELERY_` prefix. 
app.config_from_object('django.conf:settings', 
                       namespace='CELERY') 
  
# Load task modules from all registered Django app configs. 
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    # 'every 30 seconds': {
    #     'task': 'tasks.fibonacci',
    #     'schedule':  timedelta(seconds=30),
    #     'args': (10,)  # Adjust the value as needed

    # },

    'everyday at 8:00PM': {
        'task':'tasks.updateTranslation',
        'schedule': timedelta(minutes=1),
        'args':()
    }

}