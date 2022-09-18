from django.conf.urls import url
from django.urls import re_path, path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),
]
