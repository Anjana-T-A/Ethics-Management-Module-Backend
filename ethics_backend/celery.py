import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethics_backend.settings')

# Create a Celery instance
app = Celery('ethics_backend')

# Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Ensure that Django setup is called before Celery starts
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
