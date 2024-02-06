from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, F
from django.contrib.auth.models import User

from celery import shared_task
from .models import FridgeItem, Notification


@shared_task
def send_expiry_notifcations():
    now = timezone.now()

    about_to_expire_items = FridgeItem.objects.filter(
        Q(expiry_date__gt=now) | Q(expiry_date__lte=now + timedelta(days=3))
    )
    user = User.objects.filter(is_superuser=True).first()
    for item in about_to_expire_items:
        message = f"{item} item is expiring within 3 days."
        item.save()
        Notification.objects.create(
            user=user, message=message, type='item_expired')


@shared_task
def reorder():
    items_to_reorder = FridgeItem.objects.filter(
        auto_order=True, quantity__lt=F('min_reminder'))
    for item in items_to_reorder:
        item.create_order()
