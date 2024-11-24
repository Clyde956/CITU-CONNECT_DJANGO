# cituconnect/myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class MarkNotificationsAsReadMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            current_url_name = resolve(request.path_info).url_name
            if current_url_name != 'notifications':  # Handle all pages except 'notifications'
                displayed_notifications = request.session.get('displayed_notifications', [])
                if displayed_notifications:
                    request.user.notifications.filter(notification_id__in=displayed_notifications).update(isRead=True)
                    request.session['displayed_notifications'] = []
        return response