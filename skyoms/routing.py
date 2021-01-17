# -*- coding:utf-8 -*-
from channels.routing import ProtocolTypeRouter,URLRouter
import assets.routing
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(
        URLRouter(
            assets.routing.websocket_urlpatterns
        )
    )


})