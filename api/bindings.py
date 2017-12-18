import json

from channels import Group
from channels_api import list_action, detail_action
from channels_api.bindings import ResourceBinding
from rest_framework.authtoken.models import Token

from zoltan.models import Notification
from .serializers import NotificationSerializer


def get_user_from_token(token):
    """Get User from token.

    :return user : User instance or None
    """
    try:
        user = Token.objects.get(key=token).user
    except Exception:
        user = None
    return user


class NotificationBinding(ResourceBinding):

    model = Notification
    stream = "notifications"
    serializer_class = NotificationSerializer

    def deserialize(self, message):
        """Its a native method and I just add get user token from body."""
        body = json.loads(message['text'])
        self.request_id = body.get("request_id")
        action = body['action']
        if body.get('token', None):
            message.user = get_user_from_token(body.get('token', None))
        pk = body.get('pk', None)
        data = body.get('data', None)
        return action, pk, data

    def get_queryset(self):
        return Notification.objects.filter(user=self.message.user.id, read=False).order_by('-created_at')

    @detail_action()
    def subscribe(self, pk, data, **kwargs):
        """Subscribe user on his channel and return all his unread notification."""
        group_name = 'user-{}'.format(self.message.user.id)
        Group(group_name).add(self.message.reply_channel)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return serializer.data, 200

    @detail_action()
    def update(self, pk, data, **kwargs):
        """Update notification. Now we update only read param.

        :return : List with all unread Notification for current user
        """
        instance = self.get_object_or_404(pk)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serial, status = self.list(data, **kwargs)
        return serial, 200

    @list_action()
    def list(self, data, **kwargs):
        """Get all unread Notification for current user."""
        if not data:
            data = {}
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return serializer.data, 200
