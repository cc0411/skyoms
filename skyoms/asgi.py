"""
ASGI config for skyoms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skyoms.settings')
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import assets.routing
#http_application = get_asgi_application()


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            assets.routing.websocket_urlpatterns
        )
    ),

})
