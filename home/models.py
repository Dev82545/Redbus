from django.db import models
from decimal import Decimal 
from django.contrib.auth.models import User

class passengers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length= 255)
    age = models.IntegerField()
    gender = models.CharField(max_length= 255)
    
    def __str__(self):
        return self.name

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet: ${self.balance}"

