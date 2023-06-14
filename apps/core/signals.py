from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User
from .models import Account, Transaction
from .utils import send_activation_email


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        send_activation_email(instance.user)


@receiver(post_save, sender=Transaction)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        transaction_type = instance.transaction_type
        if transaction_type == "deposit":
            instance.receiver.user.send_mail(
                subject="Deposit Successful",
                message=f"You have successfully deposited ${instance.amount} to your account.",
            )
        elif transaction_type == "withdraw":
            instance.sender.user.send_mail(
                subject="Withdraw Successful",
                message=f"You have successfully withdrawn ${instance.amount} from your account.",
            )
        elif transaction_type == "transfer":
            instance.sender.user.send_mail(
                subject="Transfer Successful",
                message=f"You have successfully transferred ${instance.amount} to {instance.receiver.user.username} from your account.",
            )
            instance.receiver.user.send_mail(
                subject="Transfer",
                message=f"You have successfully received ${instance.amount} from {instance.sender.user.username} to your account.",
            )
