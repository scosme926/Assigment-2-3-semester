from django.db import models


class Seller(models.Model):
    name = models.TextField()
    country = models.TextField()
    province = models.TextField()
    city = models.TextField()

 
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.TextField()
    price = models.FloatField()
