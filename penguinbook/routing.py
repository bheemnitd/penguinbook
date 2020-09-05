from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/penguinbook/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/penguinbook/home/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]