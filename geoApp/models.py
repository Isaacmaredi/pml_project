from django.db import models
from decimal import Decimal
from pmlprofile.models import Profile

class Location(models.Model):
    member = models.CharField(max_length=200)
    address = models.CharField(max_length=350)
    lat = models.DecimalField(default=Decimal('0.0'), decimal_places=6, max_digits=8)
    lon = models.DecimalField(default=Decimal('0.0'), decimal_places=6, max_digits=8)