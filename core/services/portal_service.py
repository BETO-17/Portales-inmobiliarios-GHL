# core/services/portal_service.py
import requests
from django.conf import settings

def publish_to_portal(property_data):
    """
    Mock de publicación en portal (Adondevivir, Urbania, etc.)
    En producción: usa API real
    """
    # Mock response
    portal_id = f"portal_{property_data['ghl_id']}"
    portal_url = f"https://adondevivir.com/prop/{portal_id}"
    
    # Aquí iría requests.post() a la API real
    return {
        "success": True,
        "portal_id": portal_id,
        "portal_url": portal_url
    }