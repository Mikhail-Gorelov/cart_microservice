from django.contrib import admin
from django.contrib.admin import TabularInline

from api.v1.cart.services import ProductsService
from . import models


# Register your models here.

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic info', {'fields': ('user_id',)}),
        ('Products info', {'fields': ('custom_field',)}),
    )
    readonly_fields = ('custom_field',)

    def custom_field(self, obj):
        item_list = list(models.Item.objects.filter(cart=obj).values_list('product_variant_id'))
        converted_list = [i[0] for i in item_list]
        data = {
            'products': converted_list
        }
        print(data)
        # print(converted_list)
        # service = ProductsService(request=self.request, url='/api/v1/product-list/')
        # response = service.service_response(method="post", data=data)
        # print(response.data)
        return obj.id


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    pass
