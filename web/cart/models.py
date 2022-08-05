from django.db import models


# Create your models here.

class Cart(models.Model):
    user_id = models.PositiveIntegerField(null=True, unique=True)
    session_id = models.CharField(max_length=77, null=True, unique=True)


class Item(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    product_variant_id = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ('-created',)
