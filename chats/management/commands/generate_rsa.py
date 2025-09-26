# Python
import rsa
import os

# Django
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def generate(self):
        public_key, private_key = rsa.newkeys(nbits=2048)
        private_key_str = private_key.save_pkcs1().decode("utf-8")
        public_key_str = public_key.save_pkcs1().decode("utf-8")
        with open(f"{settings.KEYS_PATH}/public.txt", "w") as public:
            public.write(public_key_str)
        with open(f"{settings.KEYS_PATH}/private.txt", "w") as private:
            private.write(private_key_str)
        print("Keys created!")

    def handle(self, *args, **options):
        os.makedirs(settings.KEYS_PATH, exist_ok=True)
        print("Start Generate Keys")
        self.generate()
        print("Keys generated successfully")
