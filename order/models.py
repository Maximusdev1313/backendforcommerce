from django.db import models
# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=20)
    phoneNumber = models.IntegerField()
    address = models.CharField(max_length=100)
    



