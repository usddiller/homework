from __future__ import annotations

from django.db import models


class Public(models.Model):
    owner = models.ForeignKey(
        to="users.Client",
        on_delete=models.CASCADE,
        related_name="owned_publics",
        verbose_name="владелец паблика"
    )
    avatar = models.OneToOneField(
        to="images.Image",
        verbose_name="аватар пользователя",
        related_name="public_avatar",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title = models.CharField(
        verbose_name="название",
        max_length=200,
        unique=True
    )
    is_private = models.BooleanField(
        verbose_name="приватный паблик",
        default=False
    )
    members = models.ManyToManyField(
        to="users.Client",
        related_name="member_of_publics",
        verbose_name="участники"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания"
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "паблик"
        verbose_name_plural = "паблики"

    def __str__(self):
        return f"{self.owner} | {self.title} | {self.is_private}"


class PublicInvite(models.Model):
    public = models.ForeignKey(
        to=Public, 
        on_delete=models.CASCADE,
        verbose_name="паблик",
        related_name="public_invites"
    )
    invited_user = models.ForeignKey(
        to="users.Client", 
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="invites_received"
    )
    invited_by = models.ForeignKey(
        to="users.Client", 
        on_delete=models.CASCADE, 
        related_name="invites_sent",
        verbose_name="кем приглашен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата приглашения"
    )
    accepted = models.BooleanField(
        null=True,
        default=None,
        verbose_name="принято"
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "приглашение в паблик"
        verbose_name_plural = "приглашения в паблики"
        constraints = [
            models.UniqueConstraint(
                fields=["public", "invited_user", "invited_by"],
                name="unique_public_invite",
            )
        ]

    def __str__(self):
        return (f"{self.public.title} | {self.invited_user.username}" 
            f" | {self.created_at} | {self.accepted}")
