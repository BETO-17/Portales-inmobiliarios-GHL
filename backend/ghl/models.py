from django.db import models

class Property(models.Model):
    ghl_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    created_at = models.DateTimeField()