from django.db import models
from events.models import Meeting

# Create your models here.
class Minutes(models.Model):
    title = models.OneToOneField(Meeting, on_delete=models.DO_NOTHING, related_name='meeting')
    date = models.DateField(auto_now_add=True)
    doc = models.FileField(upload_to='minutes/%Y/%F')
    
    def __str__(self):
        return f'Minutes - {self.title.meeting}'
    