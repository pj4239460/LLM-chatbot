"""
This file is used to define the routing configuration for the WebSocket connections in the Django application.
"""
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # other websocket URLs here
    path(r"ws/chatgpt-demo/", consumers.ChatConsumer.as_asgi(), name="chatgpt_demo"),
]