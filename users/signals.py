from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Client, FriendInvite
from users.tasks import ActivateAccountTask


@receiver(signal=post_save, sender=Client)
def post_registration(
    sender: Client, instance: Client, created: bool, **kwargs
):
    if instance.is_superuser:
        return
    
    if created:
        ActivateAccountTask().apply_async(
            kwargs={
                "pk": instance.pk,
                "username": instance.username,
                "email": instance.email,
                "code": str(instance.activation_code),
            }
        )


@receiver(signal=post_save, sender=FriendInvite)
def remove_invites(
    instance: FriendInvite, created: bool, **kwargs
):
    if not created:
        if instance.is_accepted:
            from_client = instance.from_client
            to_client = instance.to_client
            from_client.friends.add(to_client)
            to_client.friends.add(from_client)
            from_client.save()
            to_client.save()
            
        instance.delete()