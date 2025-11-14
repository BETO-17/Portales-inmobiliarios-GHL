# core/services/portal_service.py
import requests
from django.conf import settings

def publish_to_portal(property_data):
    """
    Genera un portal_url FUNCIONAL que abre una página pública del departamento.
    En producción: puedes integrar API real (Adondevivir, etc.)
    """
    
    # === CONFIGURACIÓN DE DOMINIO ===
    # LOCAL (para pruebas)
    BASE_URL = "http://localhost:8000"
    
    # DESPLIEGUE (descomenta cuando subas a Render/Vercel)
    # BASE_URL = settings.PUBLIC_BASE_URL  # Opcional: configúralo en settings.py
    # BASE_URL = "https://depas-ghl.onrender.com"

    # === GENERAR URL PÚBLICA ===
    portal_url = f"{BASE_URL}/public/{property_data['ghl_id']}/"

    # === MOCK O API REAL (futuro) ===
    # Aquí puedes agregar requests.post() a Adondevivir, etc.
    # Por ahora: solo devolvemos el link funcional
    portal_id = f"portal_{property_data['ghl_id']}"

    return {
        "success": True,
        "portal_id": portal_id,
        "portal_url": portal_url  # ← LINK QUE ABRE LA PÁGINA REAL
    }