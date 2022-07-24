from rest_framework import serializers
from cart import models


# Create your serializers here.


class ItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, attrs):
        if attrs.get('product_id') < 1 or attrs.get('quantity') < 1:
            raise serializers.ValidationError('The value must be positive')
        return attrs


class CartShowSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_variant_id = serializers.IntegerField()
