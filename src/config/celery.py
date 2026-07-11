import os
import sys
from celery import Celery
from pathlib import Path

os.environ['REDIS_CLIENT_PROTOCOL'] = '2'

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('bank')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()