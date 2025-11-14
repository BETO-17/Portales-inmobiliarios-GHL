from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import requests
from core.models import TokenStorage

def auth_install(request):
    client_id = os.getenv('CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = "opportunities.read opportunities.write"  # + write para webhooks
    auth_url = (
        f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
        f"response_type=code&redirect_uri={redirect_uri}"
        f"&client_id={client_id}&scope={scope}"
    )
    return HttpResponseRedirect(auth_url)

@csrf_exempt
def auth_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code'}, status=400)

    token_url = f"{os.getenv('GHL_BASE_URL')}/oauth/token"
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI')
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        TokenStorage.objects.create(
            access_token=tokens['access_token'],
            refresh_token=tokens['refresh_token'],
            expires_in=tokens['expires_in']
        )
        return JsonResponse({'message': 'Autenticado'})
    return JsonResponse({'error': response.text}, status=400)