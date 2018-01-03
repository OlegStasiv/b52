from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class, route

from api.bindings import NotificationBinding


class APIDemultiplexer(WebsocketDemultiplexer):

    consumers = {
      'notifications': NotificationBinding.consumer
    }


channel_routing = [
    route_class(APIDemultiplexer)
]
