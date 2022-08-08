# Create your serializers here.
from rest_framework import serializers


class ItemOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
    product_variant_id = serializers.IntegerField(min_value=1)
