from django.db import models
from decimal import Decimal
from pmlprofile.models import Profile

class Location(models.Model):
    member = models.ForeignKey(Profile, related_name='location', on_delete=models.CASCADE)
    lat = models.DecimalField(default=Decimal('0.0'), decimal_places=6, max_digits=8)
    lng = models.DecimalField(default=Decimal('0.0'), decimal_places=6, max_digits=8)
    
    def __str__(self):
        return self.member.shortname