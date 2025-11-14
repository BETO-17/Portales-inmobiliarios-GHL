import requests
import os
from core.models import Property
from .token_service import get_valid_token

def sync_opportunities():
    token = get_valid_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Version': '2021-07-28'
    }
    url = f"{os.getenv('GHL_BASE_URL')}/opportunities/"
    params = {'limit': 50}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return {'error': response.text}

    data = response.json().get('opportunities', [])
    saved = 0
    for opp in data:
        Property.objects.update_or_create(
            ghl_id=opp['id'],
            defaults={
                'name': opp.get('title') or opp.get('name', 'Sin título'),
                'status': opp.get('status', ''),
                'price': opp.get('monetaryValue'),
            }
        )
        saved += 1
    return {'saved': saved, 'total': len(data)}