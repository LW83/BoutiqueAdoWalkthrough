from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # To receive these signals

from .models import OrderLineItem  # To listen for signals from this model

# To execute function any time the post_save signal is sent

@receiver(post_save, sender=OrderLineItem)
# Sender is here OrderLineItem instance is actual instance of model that sent it
# Created is a boolean sent by Django referring to whether this is new instance or update
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()
