# core/views/webhook.py

import hmac
import hashlib
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from core.models import Property
from core.services.portal_service import publish_to_portal


# ← MUEVE verify_signature AQUÍ (ARRIBA)
def verify_signature(payload, signature):
    if not signature:
        return False
    secret = os.getenv('WEBHOOK_SECRET').encode()
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@csrf_exempt
def ghl_webhook(request):
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        if verify_token == os.getenv('WEBHOOK_SECRET'):
            return JsonResponse({'hub.challenge': request.GET.get('hub.challenge')})
        return JsonResponse({'error': 'Invalid token'}, status=403)

    if request.method == 'POST':
        signature = request.headers.get('X-Ghl-Signature')
        if not verify_signature(request.body, signature):
            return JsonResponse({'error': 'Invalid signature'}, status=403)

        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        event = payload.get('event')
        if event != 'OpportunityUpdate':
            return JsonResponse({'status': 'ignored'})

        opp = payload.get('opportunity', {})
        if not opp or 'id' not in opp:
            return JsonResponse({'error': 'Missing opportunity data'}, status=400)

        prop, created = Property.objects.update_or_create(
            ghl_id=opp['id'],
            defaults={
                'name': opp.get('title') or opp.get('name'),
                'status': opp.get('status'),
                'price': opp.get('monetaryValue'),
                'updated_at': timezone.now()
            }
        )

        # Publicación automática
        publish_result = publish_to_portal({
            "ghl_id": prop.ghl_id,
            "name": prop.name,
            "price": str(prop.price) if prop.price else None,
            "status": prop.status
        })
        if publish_result["success"]:
            prop.portal_url = publish_result["portal_url"]
            prop.save()

        return JsonResponse({
            'status': 'updated',
            'portal_url': prop.portal_url
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)