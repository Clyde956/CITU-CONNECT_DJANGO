# cituconnect/myapp/templatetags/custom_tags.py
from django import template
from django.template.loader import render_to_string
from myapp.models import Post  # Corrected import path

register = template.Library()

@register.simple_tag(takes_context=True)
def unread_notifications_count(context, user):
    return user.notifications.filter(isRead=False).count()