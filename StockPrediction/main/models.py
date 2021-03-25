from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class Investor(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     email_id = models.EmailField(primary_key = True)
#     password = models.CharField(max_length = 50 ,editable = False)

#     def __str__(self):
#         return self.name

class Stock(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boughtStocks')
    stock_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.stock_name
    
