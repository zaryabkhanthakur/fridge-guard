from django.db import models
from django.conf import settings

class FridgeItem(models.Model):
    name = models.CharField(max_length=250, null=False)
    quantity = models.IntegerField(default=0)
    min_reminder = models.IntegerField(null=False)
    expiry_date = models.DateTimeField(null=True)
    last_added = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("FridgeItem")
        verbose_name_plural = _("FridgeItems")

    def __str__(self):
        return self.name

class FridgeHistory(models.Model):
    ACTIONS = (
        (1, "Added"),
        (2, "Removed"),
    )
    
    action = models.IntegerField(choices=ACTIONS)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(FridgeItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} {self.action} {self.item}."
    
