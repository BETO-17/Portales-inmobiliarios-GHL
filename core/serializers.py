# core/serializers.py
from rest_framework import serializers
from core.models import Property

STATUS_CHOICES = {
    'open': 'En Venta',
    'won': 'Vendido',
    'lost': 'Perdido',
}

class PropertySerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['ghl_id', 'name', 'status', 'status_display', 'price', 'portal_url', 'created_at']

    def get_status_display(self, obj):
        return STATUS_CHOICES.get(obj.status, obj.status)