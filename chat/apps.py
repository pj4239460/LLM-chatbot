"""
apps.py is a configuration file for the chat app.
"""
from django.apps import AppConfig

class ChatConfig(AppConfig):
    """
    ChatConfig is a configuration class for the chat app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
