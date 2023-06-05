"""
ASGI config for chatibility project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from channels.security.websocket import OriginValidator


from django.urls import path

from chatbots.consumer import ChatConsumer

from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatibility.settings')


print("asgi setupppppp")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(AuthMiddlewareStack(URLRouter({
        path('chat/<uuid:chat_id>', ChatConsumer.as_asgi())
        })), ["*"])
})
