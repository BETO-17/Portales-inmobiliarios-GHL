from django.urls import path
from ghl.views import InstallView, CallbackView

urlpatterns = [
    path('auth/install', InstallView.as_view()),
    path('auth/callback', CallbackView.as_view()),
]
