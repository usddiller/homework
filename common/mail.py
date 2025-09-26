import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from loguru import logger


def send_email(
    template: str, 
    to: str | list[str], title: str,
    context: dict | None = None
):
    try:
        text = strip_tags(value=template).strip()
        text_content = render_to_string(
            template_name=template, context=context,
        )
        html_content = render_to_string(
            template_name=template, context=context,
        )
        msg = EmailMultiAlternatives(
            subject=title, body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[to] if isinstance(to, str) else to,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
        raise