# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_fridge.settings')

celery = Celery('smart_fridge')

celery.config_from_object('django.conf:settings', namespace='CELERY')

celery.autodiscover_tasks()
