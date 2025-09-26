from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(
        verbose_name="категория", unique=True, max_length=50
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.pk} | {self.title}"


class Post(models.Model):
    title = models.CharField(
        verbose_name="Название поста",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=5000,
    )
    date_publication = models.DateTimeField(
        verbose_name="дата публикации",
        default=timezone.now,
    )
    user = models.ForeignKey(
        to="users.Client",
        verbose_name="автор",
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    categories = models.ManyToManyField(
        to=Category,
        verbose_name="категории",
        related_name="post_categories",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"], name="unique_post"
            )
        ]

    def __str__(self):
        return f"{self.title} | {self.date_publication}"


class PostImage(models.Model):
    image = models.ForeignKey(
        to="images.Image",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="изображение",
        blank=True,
        related_name="post_usage"
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="статья",
    )
    position = models.PositiveIntegerField(
        verbose_name="позиция в статье",
        default=0,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return f"{self.pk} | {self.image}"
