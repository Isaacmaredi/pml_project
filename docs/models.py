from django.db import models
from events.models import Meeting

class Minutes(models.Model):
    title = models.OneToOneField(Meeting, on_delete=models.DO_NOTHING, related_name='meeting')
    date = models.DateField(auto_now_add=True)
    doc = models.FileField(upload_to='minutes/%Y/%F')
    
    def __str__(self):
        return f'Minutes - {self.title.meeting}'

class Policy(models.Model):
    title = models.CharField(max_length=250)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    doc_file = models.FileField(upload_to='policies/%Y/%F')
    
class Report(models.Model):
    title = models.CharField(max_length=250)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    doc = models.FileField(upload_to='reports/%Y/%F')


    