from uuid import uuid4
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, connection
from typing import NamedTuple
from order.choices import OrderStatus


def get_order_number():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('order_order_number_seq')")
        result = cursor.fetchone()
        return result[0]


class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    number = models.IntegerField(unique=True, default=get_order_number, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=32, default=OrderStatus.UNFULFILLED, choices=OrderStatus.CHOICES
    )
    user_id = models.PositiveIntegerField(null=True, blank=True)
    session_id = models.CharField(max_length=200, null=True, blank=True)
    billing_address_id = models.PositiveIntegerField(null=True, blank=True)
    shipping_address_id = models.PositiveIntegerField(null=True, blank=True)
    user_email = models.EmailField(blank=True, default="")
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
    )
    channel_id = models.PositiveIntegerField()
    customer_note = models.TextField(blank=True, default="")


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, related_name="lines", editable=False, on_delete=models.CASCADE
    )
    product_variant_id = models.PositiveIntegerField(null=True)
    product_name = models.CharField(max_length=386)
    variant_name = models.CharField(max_length=255, default="", blank=True)
    product_sku = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_fulfilled = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
    )


class OrderLineData(NamedTuple):
    order: Order
    product_variant_id: int
    product_name: str
    variant_name: str
    product_sku: str
    quantity: int
    currency: str
