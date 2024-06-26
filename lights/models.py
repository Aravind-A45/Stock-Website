from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=300)
    net = models.CharField(max_length=300)
    price = models.CharField(max_length=300)
    qty = models.PositiveIntegerField()
    qty_aval = models.PositiveIntegerField()

class Division(models.Model):
    name = models.CharField(max_length=300)   

class Cart(models.Model):
    stock_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
      return self.stock_name.name

class MyBuys(models.Model):
    stock_products = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
  