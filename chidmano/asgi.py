"""
ASGI config for chidmano project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from store_analysis import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')

# Import URL patterns for WebSocket routing
from django.urls import re_path
from store_analysis.consumers import AnalysisConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/analysis/(?P<analysis_id>\w+)/$', AnalysisConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
}) 