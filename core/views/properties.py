# core/views/properties.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import Property  # ← ABSOLUTO
from core.serializers import PropertySerializer  # ← ABSOLUTO
from core.services.portal_service import publish_to_portal
from django.utils import timezone

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extraer datos
        data = serializer.validated_data
        ghl_id = data['ghl_id']

        # Crear o actualizar
        prop, created = Property.objects.update_or_create(
            ghl_id=ghl_id,
            defaults={
                'name': data.get('name'),
                'status': data.get('status', 'open'),
                'price': data.get('price'),
                'updated_at': timezone.now()
            }
        )

        # Publicar si es nuevo
        if created or not prop.portal_url:
            result = publish_to_portal({
                "ghl_id": prop.ghl_id,
                "name": prop.name,
                "price": str(prop.price) if prop.price else None,
                "status": prop.status
            })
            if result["success"]:
                prop.portal_url = result["portal_url"]
                prop.save()

        # Devolver con serializer
        return Response({
            "message": "Departamento creado/actualizado",
            "property": PropertySerializer(prop).data
        }, status=status.HTTP_201_CREATED)