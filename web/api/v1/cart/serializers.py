from rest_framework import serializers

from api.v1.cart.services import ProductsService
from cart import models


# Create your serializers here.


class ItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    product_variant_id = serializers.IntegerField(min_value=1)


class CartShowSerializer(serializers.Serializer):
    product_variant_id = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()

    def get_product_variant_id(self, obj):
        var_id = obj.product_variant_id
        service = ProductsService(request=self.context['request'], url=f"/api/v1/product-variant/{var_id}/")
        response = service.service_response(method="get")
        return response.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_variant_id']['quantity'] = data['quantity']
        return data['product_variant_id']
