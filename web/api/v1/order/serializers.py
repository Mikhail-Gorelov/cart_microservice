# Create your serializers here.
from rest_framework import serializers
from order.models import Order, OrderLine


class ItemOrderSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    product_variant_id = serializers.IntegerField(min_value=1)


class DraftOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = (
            'product_variant_id', 'product_name', 'variant_name',
            'product_sku', 'quantity', 'quantity_fulfilled', 'currency'
        )


class DraftOrderSerializer(serializers.ModelSerializer):
    lines = DraftOrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'created', 'updated_at', 'lines')


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = (
            'id',
            'product_variant_id',
            'product_name',
            'variant_name',
            'product_sku',
            'quantity',
            'currency',
            'price'
        )


class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'number', 'created', 'updated_at', 'status', 'currency', 'total_sum')
