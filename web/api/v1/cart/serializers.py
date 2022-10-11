from django.db.models import Sum
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


class CartTotalSerializer(serializers.Serializer):
    total_sum = serializers.SerializerMethodField()
    items_number = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()

    def get_total_sum(self, obj):
        variant_ids = [i[0] for i in list(obj.items.all().values_list('product_variant_id'))]
        service = ProductsService(request=self.context['request'], url=f"/api/v1/total-sum/")
        response = service.service_response(method="post", data={'variant_ids': variant_ids})
        return response.data.get('total_sum')

    def get_items_number(self, obj):
        return obj.items.all().count()

    def get_total_weight(self, obj):
        variant_ids = [i[0] for i in list(obj.items.all().values_list('product_variant_id'))]
        service = ProductsService(request=self.context['request'], url=f"/api/v1/total-weight/")
        response = service.service_response(method="post", data={'variant_ids': variant_ids})
        return response.data.get('total_weight')
