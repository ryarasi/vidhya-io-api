from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from .schema import MyGraphqlWsConsumer

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
            URLRouter(
                [path("graphql/", MyGraphqlWsConsumer.as_asgi())]
            )
        )),
    }
)
