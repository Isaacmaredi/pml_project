from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name 