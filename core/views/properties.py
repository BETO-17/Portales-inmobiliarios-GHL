from django.http import JsonResponse
from core.services.ghl_service import sync_opportunities
from core.models import Property
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def sync_view(request):
    result = sync_opportunities()
    return Response(result)

@api_view(['GET'])
def list_properties(request):
    props = Property.objects.values(
        'ghl_id', 'name', 'status', 'price', 'updated_at'
    ).order_by('-updated_at')[:20]
    return Response(list(props))