from django import template

register = template.Library()

@register.filter()
def check_permission(user, permission):
    print(permission)
    return user.user_permissions.filter(codename=permission).exists()