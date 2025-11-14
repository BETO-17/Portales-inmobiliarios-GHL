# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.auth import auth_install, auth_callback
from .views.webhook import ghl_webhook
from .views.publish import publish_property
from .views.properties import PropertyViewSet
from .views.public import public_property  # ← NUEVO

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    path('auth/install/', auth_install),
    path('auth/callback/', auth_callback),
    path('webhook/ghl/', ghl_webhook),
    path('publish/<str:ghl_id>/', publish_property),
    path('public/<str:ghl_id>/', public_property),  # ← RUTA PÚBLICA
]

urlpatterns += router.urls