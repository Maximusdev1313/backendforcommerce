
from django.db import models
# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=20)
    phoneNumber = models.IntegerField()
    address = models.CharField(max_length=100)
    total = models.IntegerField()
    comment = models.TextField(max_length = 300, blank=True, null=True)
    ready = models.CharField(max_length=50)
    def __str__(self):
        return self.userName

class Order(models.Model):
    product_name = models.CharField(max_length=100)
    weight = models.FloatField( blank=True)
    litr = models.FloatField( blank=True)
    quantity = models.IntegerField( blank=True)
    summa = models.FloatField()
    orderForUser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orderForUser')

    def __str__(self):
        return self.product_name




