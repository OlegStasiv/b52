import json

from channels import Group
from django.contrib import admin

from api.serializers import NotificationSerializer
from zoltan.models import Notification


class NotificationList(admin.ModelAdmin):
    model = Notification
    list_display = ("id", "user", "text", "read",)

    def save_model(self, request, obj, form, change):
        """When we save new notification in admin we send a list with notifications to user through websocket"""
        obj.save()
        serializer = NotificationSerializer(Notification.objects.filter(user=obj.user_id, read=False).order_by('-created_at'), many=True)
        payload = {
            "stream": "notifications",
            'payload': {
                'data': serializer.data,
                'action': 'create',
                'response_status': 200,
                },
        }

        Group("user-%s" % obj.user_id).send({'text': json.dumps(payload)})


admin.site.register(Notification, NotificationList)
