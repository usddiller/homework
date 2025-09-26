import os

from celery import Celery
from celery.schedules import crontab

from decouple import config


REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "settings.settings"
)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
app: Celery = Celery(main="proj", broker=REDIS_URL, backend=REDIS_URL)
app.autodiscover_tasks()
app.conf.timezone = "Asia/Almaty"
# app.conf.beat_schedule = {
    # "congratulations": {
    #     "task": "send-congrats",
    #     "schedule": crontab(hour=20, minute=46)
    # }
# }
