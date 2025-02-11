from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone =models.CharField(max_length= 255)
    
    def __str__(self):
        return self.name
# Create your models here.
