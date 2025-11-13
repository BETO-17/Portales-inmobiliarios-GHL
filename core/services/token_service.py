import requests
import os
from django.conf import settings
from core.models import TokenStorage

def get_valid_token():
    try:
        token = TokenStorage.objects.latest('created_at')
        # Si expira en < 5 min, refrescar
        if token.expires_in < 300:
            return refresh_token(token.refresh_token)
        return token.access_token
    except TokenStorage.DoesNotExist:
        raise Exception("No hay token. Autenticar primero.")

def refresh_token(refresh_token):
    url = f"{os.getenv('GHL_BASE_URL')}/oauth/token"
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        TokenStorage.objects.create(
            access_token=tokens['access_token'],
            refresh_token=tokens['refresh_token'],
            expires_in=tokens['expires_in']
        )
        return tokens['access_token']
    raise Exception("Fallo al refrescar token")