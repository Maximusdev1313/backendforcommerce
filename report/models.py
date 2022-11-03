from django.db import models

# Create your models here.

class ProductList(models.Model):
    product_name = models.TextField(max_length=100, null=True, blank=True)
    weight = models.TextField(blank=True, null=True)
    quantity = models.TextField(blank=True, null=True)
    litr  = models.TextField(blank=True, null=True)
    price = models.TextField(null=True, blank=True)
    total_price = models.TextField(null=True, blank=True)
    residue = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.product_name

class Score(models.Model):
    # bir oylik buyurtmalar soni 
    orders = models.TextField(null=True, blank=True) 
    # aylanma mablag'  
    working_kapital = models.TextField(null=True, blank=True)
    # bir oylik foyda 
    benefit  = models.TextField(null=True, blank=True)
    # soliqlar 
    taxes = models.TextField(null=True, blank=True)
    # chiqimlar 
    expenses = models.TextField(null=True, blank=True)
    # ishchilar uchun oylik to'lovlar 
    salary = models.TextField(null=True, blank=True)
    # amartizatsiya / kutilmagan narx ozgarishi va rasxodlar uchun ajratma mablag'
    amortization = models.TextField(null=True, blank=True)
    # sof foyda
    profit = models.TextField(null=True, blank=True)
    #  o'tgan oyga nisbatan korilgan foyda
    diversity = models.TextField(null=True, blank=True)

    # o'tgan oygi foyda
    lastProfit = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.working_kapital
