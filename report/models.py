from django.db import models

# Create your models here.

class ProductList(models.Model):
    product_name = models.CharField(max_length=100)
    weight = models.FloatField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    litr  = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    total_price = models.FloatField()
    residue = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.product_name

class Score(models.Model):
    # bir oylik buyurtmalar soni 
    orders = models.FloatField() 
    # aylanma mablag'  
    working_kapital = models.FloatField()
    # bir oylik foyda 
    benefit  = models.FloatField()
    # soliqlar 
    taxes = models.FloatField()
    # chiqimlar 
    expenses = models.FloatField()
    # ishchilar uchun oylik to'lovlar 
    salary = models.FloatField()
    # amartizatsiya / kutilmagan narx ozgarishi va rasxodlar uchun ajratma mablag'
    amortization = models.FloatField()
    # sof foyda
    profit = models.FloatField()
    #  o'tgan oyga nisbatan korilgan foyda
    diversity = models.FloatField()

    # o'tgan oygi foyda
    lastProfit = models.FloatField()

    def __str__(self):
        return self.working_kapital
