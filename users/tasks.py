from celery import Task

from common.mail import send_email
from settings import celery_app


class ActivateAccountTask(Task):
    name = "activate-account"
    default_retry_delay = 60

    def run(self, pk:int, username: str, email: str, code: str):
        try:
            send_email(
                template="activation.html", to=email,
                context={
                    "username": username,
                    "code": (f"http://89.207.252.80/activate/{pk}/?code={code}"),
                },
                title="Confirm your account",
            )
        except Exception as e:
            raise self.retry(
                exc=e, 
                countdown=60 * (self.request.retries + 1)
            )


celery_app.register_task(task=ActivateAccountTask())
