import time
from datetime import timedelta

from loguru import logger

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from users.models import Client


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, required=False)

    def generate(self, *args, **options):
        count = options.get("count")
        if not count:
            count = 100
        objs = []
        for i in range(count):
            objs.append(Client(
                username=f"user_{i+1}",
                email=f"user_{i+1}@gmail.com",
                password=make_password("qwerty123"),
                is_active=True,
                expired_code=timezone.now() + timedelta(minutes=3)
            ))
            logger.info(f"Создал объект {i+1}")
        logger.info("Я работаю")
        Client.objects.bulk_create(
            objs=objs, ignore_conflicts=False,
            batch_size=500
        )

    def handle(self, *args, **options):
        logger.info("Start Generate Users")
        start = time.perf_counter()
        self.generate(*args, **options)
        logger.info("Users generated successfully")
        end = time.perf_counter()
        logger.info(f"Выполнено за {end-start:.4f} секунды")
