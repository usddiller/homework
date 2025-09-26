import os
import uuid

from django.db import models
from django.db.models import Q, CheckConstraint


def image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"

    if hasattr(instance, "user_avatar"):
        return f"avatars/users/{unique_name}"
    elif hasattr(instance, "public_avatar"):
        return f"avatars/publics/{unique_name}"
    elif hasattr(instance, "post_usage"):
        return f"posts/{unique_name}"
    return f"misc/{unique_name}"


class Image(models.Model):
    image = models.ImageField(
        verbose_name="изображение",
        upload_to=image_upload_to,
    )
    created_at = models.DateTimeField(
        verbose_name="дата создания", auto_now_add=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self) -> str:
        return f"{self.pk} -> {self.created_at}"


class Gallery(models.Model):
    user = models.OneToOneField(
        to="users.Client",
        on_delete=models.CASCADE,
        related_name="user_gallery",
        blank=True,
        null=True,
        verbose_name="пользователь",
    )
    public = models.OneToOneField(
        to="publics.Public",
        on_delete=models.CASCADE,
        related_name="public_gallery",
        blank=True,
        null=True,
        verbose_name="паблик",
    )
    images = models.ManyToManyField(
        to=Image,
        related_name="gallery_usage",
        verbose_name="изображения",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "галлерея"
        verbose_name_plural = "галлереи"
        constraints = [CheckConstraint(
            check=(
                (Q(user__isnull=False) & Q(public__isnull=True))
                | (Q(user__isnull=True) & Q(public__isnull=False))
            ),
            name="only_user_or_public",
        )]

    def __str__(self):
        return f"{self.pk}"
