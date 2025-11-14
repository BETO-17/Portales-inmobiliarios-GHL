# core/views/publish.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Property
from core.services.portal_service import publish_to_portal

@api_view(['POST'])
def publish_property(request, ghl_id):
    try:
        prop = Property.objects.get(ghl_id=ghl_id)
        result = publish_to_portal({
            "ghl_id": prop.ghl_id,
            "name": prop.name,
            "price": str(prop.price),
            "status": prop.status
        })
        
        if result["success"]:
            # Opcional: guarda portal_url en modelo
            prop.portal_url = result["portal_url"]
            prop.save()
            return Response({
                "message": "Publicado en portal",
                "portal_url": result["portal_url"]
            })
        else:
            return Response({"error": "Fallo en portal"}, status=500)
    except Property.DoesNotExist:
        return Response({"error": "Propiedad no encontrada"}, status=404)