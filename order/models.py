
from django.db import models
# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=20, null=True, blank=True)
    phoneNumber = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    comment = models.TextField(max_length = 300, blank=True, null=True)
    ready = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.userName

class Order(models.Model):
    product_name = models.CharField(max_length=100)
    weight = models.FloatField( blank=True, null=True)
    litr = models.FloatField( blank=True,null=True)
    quantity = models.IntegerField( blank=True,null=True)
    price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    orderForUser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orderForUser')

    def __str__(self):
        return self.product_name




