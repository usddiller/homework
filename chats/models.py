from django.db import models
from django.db.models import Q, CheckConstraint


class Chat(models.Model):
    is_group = models.BooleanField(
        verbose_name="групповой чат", default=False
    )
    title = models.CharField(
        verbose_name="заголовок", max_length=100, blank=True, null=True
    )
    users = models.ManyToManyField(
        to="users.Client",
        related_name="users_chats",
        verbose_name="пользователи",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "чат"
        verbose_name_plural = "чаты"
        constraints = [
            CheckConstraint(
                check=(
                    Q(is_group=False)
                    | (Q(is_group=True) & Q(title__isnull=False))
                ),
                name="group_chat_requires_title",
            )
        ]

    def __str__(self):
        return f"{self.pk} -> {self.is_group}"


class Message(models.Model):
    text = models.TextField(
        verbose_name="текст",
        max_length=2000,
    )
    sender = models.ForeignKey(
        to="users.Client",
        verbose_name="отправитель",
        on_delete=models.SET_NULL,
        null=True,
        related_name="messages_sender",
    )
    chat = models.ForeignKey(
        to=Chat,
        verbose_name="чат",
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    sent_at = models.DateTimeField(
        auto_now_add=True, verbose_name="отправлено"
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        verbose_name="ответ на...",
        related_name="parent_message",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self):
        return (
            f"{self.text[:20]} | {self.sender} "
            f"| {self.sent_at} | {self.chat}"
        )
