import json

from channels import Group

from zoltan.models import Notification
from api.serializers import NotificationSerializer


def send_notification_to_user(user, text):
    """Create and send notification to user.

    :param user : User instance
    :param text : Text for notification
    """

    Notification.objects.create(user=user, text=text)
    serializer = NotificationSerializer(Notification.objects.filter(user=user.id, read=False).order_by('-created_at'), many=True)
    payload = {
            "stream": "notifications",
            'payload': {
                'data': serializer.data,
                'action': 'create',
                'response_status': 200,
                },
    }

    Group("user-%s" % user.id).send({'text': json.dumps(payload)})


def send_points_count_to_user(user, point_count):
    """Send new point value to user by socket.

    :param user : User instance
    :param point_count : Point count
    """

    payload = {
        "stream": "points",
        'payload': {
            'data': {'point': point_count},
            'action': 'update',
            'response_status': 200,
        },
    }

    Group("user-%s" % user.id).send({'text': json.dumps(payload)})
