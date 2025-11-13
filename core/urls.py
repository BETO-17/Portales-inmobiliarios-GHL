# core/urls.py
from django.urls import path

# Importa desde los subarchivos
from .views.auth import auth_install, auth_callback
from .views.properties import sync_view, list_properties
from .views.webhook import ghl_webhook
from .views.publish import publish_property

urlpatterns = [
    path('auth/install/', auth_install),
    path('auth/callback/', auth_callback),
    path('sync/', sync_view),
    path('properties/', list_properties),
    path('webhook/ghl/', ghl_webhook),
    path('publish/<str:ghl_id>/', publish_property),
]