# Generated by Django 3.2.13 on 2022-08-02 17:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import order.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=order.models.get_order_number, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unconfirmed', 'Unconfirmed'), ('unfulfilled', 'Unfulfilled'), ('partially fulfilled', 'Partially fulfilled'), ('partially_returned', 'Partially returned'), ('returned', 'Returned'), ('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='unfulfilled', max_length=32)),
                ('user_id', models.PositiveIntegerField(blank=True, null=True)),
                ('billing_address_id', models.PositiveIntegerField(blank=True, null=True)),
                ('shipping_address_id', models.PositiveIntegerField(blank=True, null=True)),
                ('user_email', models.EmailField(blank=True, default='', max_length=254)),
                ('currency', models.CharField(max_length=3)),
                ('channel_id', models.PositiveIntegerField()),
                ('customer_note', models.TextField(blank=True, default='')),
            ],
        ),
        # define auto incrementing for order number field
        migrations.RunSQL(
            """
            CREATE SEQUENCE order_order_number_seq OWNED BY order_order.number;

            SELECT setval('order_order_number_seq', coalesce(max(number), 0) + 1, false)
            FROM order_order;
        """
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_variant_id', models.PositiveIntegerField(null=True)),
                ('product_name', models.CharField(max_length=386)),
                ('variant_name', models.CharField(blank=True, default='', max_length=255)),
                ('product_sku', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity_fulfilled', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('currency', models.CharField(max_length=3)),
                ('order', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.order')),
            ],
        ),
    ]
