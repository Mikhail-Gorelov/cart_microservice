from django.db.models import Sum
from urllib.parse import parse_qsl
from rest_framework import serializers

from api.v1.cart.services import ProductsService


# Create your serializers here.


class ItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    product_variant_id = serializers.IntegerField(min_value=1)


class ItemDeleteSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField(min_value=1)


class ItemChangeQuantitySerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField()


class ItemShowQuantitySerializer(serializers.Serializer):
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
    currency = serializers.SerializerMethodField()

    def get_total_sum(self, obj):
        variant_ids = list(obj.items.all().values_list('product_variant_id', flat=True))
        service = ProductsService(request=self.context['request'], url=f"/api/v1/total-sum/")
        response = service.service_response(method="post", data={'variant_ids': variant_ids})
        items_dict = dict(obj.items.all().values_list('product_variant_id', 'quantity'))
        multiplied_dict = {}
        for k, v in response.data.items():
            multiplied_dict[k] = v * items_dict[int(k)]
        return sum(multiplied_dict.values())

    def get_items_number(self, obj):
        return obj.items.all().aggregate(Sum('quantity')).get('quantity__sum')

    def get_total_weight(self, obj):
        variant_ids = list(obj.items.all().values_list('product_variant_id', flat=True))
        quantity = list(obj.items.all().values_list('quantity', flat=True))
        output_list = []
        for index, value in enumerate(variant_ids):
            output_list.append({
                'variant_id': value,
                'quantity': quantity[index]
            })
        service = ProductsService(request=self.context['request'], url=f"/api/v1/total-weight/")
        response = service.service_response(method="post", json=output_list)
        return response.data.get('total_weight')

    def get_currency(self, obj):
        if reg_country := dict(parse_qsl(self.context['request'].COOKIES.get('reg_country'))):
            return reg_country.get('currency_code')
        return None
