
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    nomi = models.CharField(max_length=100)
    kilogramm = models.CharField( max_length=100, null=True, blank=True)
    litri = models.CharField(max_length=100,  null=True, blank=True)
    soni = models.CharField(max_length=100, null=True, blank=True)
    narx = models.CharField(max_length=100)
    chegirma_narx = models.CharField(max_length=64, null=True, blank=True)
    chegirma_foizi = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, )
    mahsulot = models.ForeignKey('Categoriya', on_delete=models.CASCADE, related_name='mahsulot')

    def __str__(self):
        return self.nomi
class ProductRasmi(models.Model):
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=2500, null=True)
    rasmlari = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='rasmlari')
    def __str__(self):
        return self.title


class Categoriya(models.Model):
    categoriya_nomi = models.CharField(max_length=200)
    
    def __str__(self):
        return self.categoriya_nomi  
class CategoriyaRasm(models.Model):
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=2500, null=True)
    rasmlar = models.ForeignKey('Categoriya', on_delete=models.CASCADE, related_name='rasmlar')
    def __str__(self):
        return self.title
