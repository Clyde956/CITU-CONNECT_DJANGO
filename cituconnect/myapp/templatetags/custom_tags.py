# cituconnect/myapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def unread_notifications_count(context, user):
    return user.notifications.filter(isRead=False).count()