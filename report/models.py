from django.db import models

# Create your models here.

class Report(models.Model):
    product_name = models.CharField(max_length=100)
    weight = models.FloatField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    litr  = models.FloatField(blank=True, null=True)
    summa = models.FloatField()
    totalSumma = models.FloatField()
    def __str__(self):
        return self.product_name