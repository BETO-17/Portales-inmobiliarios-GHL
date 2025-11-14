from django.db import models

class TokenStorage(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

# core/models.py
class Property(models.Model):
    ghl_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    portal_url = models.URLField(blank=True, null=True)  # ← NUEVO
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"