from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


ORDER_STATUS = (
    ("processing", "Processing"),
    ("delivered", "Delivered"),
)

NOTIFICATION_TYPE = (
    (
        ("order_delivered", "Order Delivered"),
        ("order_placed", "New Order Placed"),
        ("item_expired", "Item Expired"),
        ("item_removed", "Item Removed"),
        ("item_inserted", "Item Inserted"),
        ("fridge_opened", "Fridge opened"),
        ('out_of_order', "Out of Order")
    )
)
CODE_LENGTH = 12


def generate_rider_password():
    return get_random_string(CODE_LENGTH)


class Suplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=16, null=True)

    def __str__(self):
        return self.name


class FridgeItem(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    quantity = models.IntegerField(default=0)
    min_reminder = models.IntegerField(null=False)
    supplier = models.ForeignKey(Suplier, null=True, on_delete=models.SET_NULL)
    default_order_quantity = models.PositiveIntegerField(null=False)
    expiry_date = models.DateTimeField(null=True)
    last_added = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_order = models.BooleanField(null=False, default=True)
    is_expired = models.BooleanField(null=False, default=False)
    constraints = [
        models.UniqueConstraint(fields=['name'], name="unique_item")
    ]

    class Meta:
        verbose_name = "FridgeItem"
        verbose_name_plural = "FridgeItems"

    def create_order(self):
        new_order = Order.objects.create(
            fridge_item=self, supplier=self.supplier, quantity=self.default_order_quantity)
        superuser = User.objects.filter(is_superuser=True).first()
        message = f"{superuser} has been ordered {self.default_order_quantity} of {self}."
        _notf = Notification.objects.create(
            user=superuser, type="order_placed", message=message)
        return new_order

    def take_item(self, amount, user):
        self.quantity -= amount
        superuser = User.objects.filter(is_superuser=True).first()
        message = f"{user} has been taken {amount} of {self}, Remaining quantity {self.quantity}"
        _notf = Notification.objects.create(
            user=superuser, type="item_removed", message=message)
        self.save()

    def insert_item(self, amount, user):
        self.quantity += amount
        superuser = User.objects.filter(is_superuser=True).first()
        message = f"{user} has been inserted {amount} of {self}, Remaining quantity {self.quantity}"
        _notf = Notification.objects.create(
            user=superuser, type="item_inserted", message=message)
        self.save()

    def __str__(self):
        return self.name


class Order(models.Model):
    firdge_item = models.ForeignKey(
        FridgeItem, null=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suplier, null=True, on_delete=models.SET_NULL)
    order_code = models.CharField(
        max_length=CODE_LENGTH, editable=False, default=generate_rider_password)
    order_status = models.CharField(
        max_length=30, choices=ORDER_STATUS, default="processing")
    quantity = models.PositiveIntegerField(null=False)
    expiry_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_order_statue(self):
        self.update(order_status='Delivered')

        self.firdge_item.update(expiry_date=self.expiry_date)
        superuser = User.objects.filter(is_superuser=True).first()
        message = f"{self} has been delieverd"
        notification = Notification.objects.create(
            user=superuser, type="order_delivered", message=message)

    def save(self, *args, **kwargs):
        superuser = User.objects.filter(is_superuser=True).first()
        message = f"{self} has been created"
        notification = Notification.objects.create(
            user=superuser, type="order_delivered", message=message)

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.firdge_item} ordered from {self.supplier} in {self.quantity}."


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
