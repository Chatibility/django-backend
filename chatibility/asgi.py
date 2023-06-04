"""
ASGI config for chatibility project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from django.urls import path

from chatbots.consumer import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatibility.settings')


print("asgi setupppppp")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter({
        path('chat/<uuid:chat_id>', ChatConsumer.as_asgi())
    })
})
