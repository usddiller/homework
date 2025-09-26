from django.db import models
from django.db.models import Q
from django.utils import timezone


class Comments(models.Model):
    post = models.ForeignKey(
        to="posts.Post",
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name="статья",
    )
    user = models.ForeignKey(
        to="users.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_comments",
        verbose_name="автор комментария",
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_comments",
        verbose_name="родительский комментарий",
    )
    text = models.TextField(
        verbose_name="текст комментария",
        max_length=2000,
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"{self.user} | {self.text[:20]}..."


class LikeDislike(models.Model):
    user = models.ForeignKey(
        to="users.Client",
        on_delete=models.CASCADE,
        verbose_name="кто оценил",
    )

    user_avatar = models.ForeignKey(
        to="images.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes_on_user_avatar",
    )
    public_avatar = models.ForeignKey(
        to="images.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes_on_public_avatar",
    )
    gallery_image = models.ForeignKey(
        to="images.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes_on_gallery_image",
    )

    is_like = models.BooleanField(
        verbose_name="лайк?", help_text="True — лайк, False — дизлайк"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(user_avatar__isnull=False)
                    | Q(public_avatar__isnull=False)
                    | Q(gallery_image__isnull=False)
                ),
                name="at_least_one_target",
            ),
            models.CheckConstraint(
                check=~(
                    (
                        Q(user_avatar__isnull=False)
                        & Q(public_avatar__isnull=False)
                    )
                    | (
                        Q(user_avatar__isnull=False)
                        & Q(gallery_image__isnull=False)
                    )
                    | (
                        Q(public_avatar__isnull=False)
                        & Q(gallery_image__isnull=False)
                    )
                ),
                name="only_one_target",
            ),
            models.UniqueConstraint(
                fields=["user", "user_avatar"],
                name="unique_user_avatar_like",
            ),
            models.UniqueConstraint(
                fields=["user", "public_avatar"],
                name="unique_public_avatar_like",
            ),
            models.UniqueConstraint(
                fields=["user", "gallery_image"],
                name="unique_gallery_image_like",
            ),
        ]

    def __str__(self):
        target = (
            self.user_avatar or self.public or self.gallery_image or "???"
        )
        return f"{self.user} → {'лайк' if self.is_like else 'дизлайк'} для {target}"
