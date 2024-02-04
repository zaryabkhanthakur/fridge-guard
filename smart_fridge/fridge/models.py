from django.db import models
from django.conf import settings


class Suplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=16, null=True)
    
    def __str__(self):
        return self.name

class FridgeItem(models.Model):
    name = models.CharField(max_length=250, null=False)
    quantity = models.IntegerField(default=0)
    min_reminder = models.IntegerField(null=False)
    expiry_date = models.DateTimeField(null=True)
    last_added = models.DateTimeField(null=True)
    suplier = models.ForeignKey(Suplier, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FridgeItem"
        verbose_name_plural = "FridgeItems"

    def __str__(self):
        return self.name

class FridgeHistory(models.Model):
    ACTIONS = (
        ('added', "Added"),
        ('removed', "Removed"),
    )
    
    action = models.CharField(max_length=10, choices=ACTIONS)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(FridgeItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} {self.action} {self.item}."
    
