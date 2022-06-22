from django.db import models


# Create your models here.

class Cart(models.Model):
    user_id = models.PositiveIntegerField()


class Item(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
