from .models import Notification

def dynamic_context(request):
    if request.user.is_superuser:
        notification_count = Notification.objects.filter(is_read=False).count()
        
        return {"notification_count": notification_count}
    return {}