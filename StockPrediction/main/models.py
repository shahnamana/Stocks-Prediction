from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Stock(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boughtStocks')
    stock_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.stock_name
    
