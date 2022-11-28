
from email.policy import default
from time import time
from django.db import models
# from pytz import timezone
from django.utils import timezone
# Create your models here.

class User(models.Model):
    ip_address = models.CharField(blank=True, null=True, max_length=50)
    userName = models.TextField(max_length=20, null=True, blank=True)
    phoneNumber = models.TextField(null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    location = models.TextField(max_length=100, null=True, blank=True)
    total = models.TextField(null=True, blank=True)
    comment = models.TextField(max_length = 300, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, )
    ready = models.TextField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.userName

class Order(models.Model):
    product_name = models.TextField(max_length=100)
    weight = models.TextField( blank=True, null=True)
    litr = models.TextField( blank=True,null=True)
    quantity = models.TextField( blank=True,null=True)
    price = models.TextField(null=True, blank=True)
    total_price = models.TextField(null=True, blank=True)
    orderForUser = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orderForUser')

    def __str__(self):
        return self.product_name




