# core/views/public.py
from django.shortcuts import render, get_object_or_404
from core.models import Property

STATUS_CHOICES = {
    'open': 'En Venta',
    'won': 'Vendido',
    'lost': 'Perdido',
}

def public_property(request, ghl_id):
    prop = get_object_or_404(Property, ghl_id=ghl_id)
    status_display = STATUS_CHOICES.get(prop.status, prop.status)
    status_class = 'en-venta' if prop.status == 'open' else 'vendido' if prop.status == 'won' else 'perdido'
    
    return render(request, 'public_property.html', {
        'name': prop.name,
        'price': f"{prop.price:,.0f}" if prop.price else "Consultar",
        'ghl_id': prop.ghl_id,
        'status_display': status_display,
        'status_class': status_class
    })