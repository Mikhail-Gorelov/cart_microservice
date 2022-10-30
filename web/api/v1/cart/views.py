import logging

from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from cart import models
from . import serializers
from .services import CartHandler, ProductsService

logger = logging.getLogger(__name__)


# Create your views here.

class CartAddView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user_id = self.request.remote_user.id
        try:
            obj = models.Cart.objects.get(user_id=user_id)
        except models.Cart.DoesNotExist:
            obj = models.Cart(user_id=user_id)
            obj.save()
        return Response({'cart_id': obj.pk})


class ItemAddView(GenericAPIView):
    serializer_class = serializers.ItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.remote_user.id
        cart = models.Cart.objects.get(user_id=user_id)
        models.Item.objects.create(cart=cart, **serializer.data)
        return Response(serializer.data)


class ItemDeleteView(GenericAPIView):
    serializer_class = serializers.ItemDeleteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.remote_user.id
        cart = models.Cart.objects.get(user_id=user_id)
        item = models.Item.objects.get(cart=cart, **serializer.data)
        # item = models.Item.objects.filter(cart=cart, **serializer.data)
        item.delete()
        return Response(serializer.data)


class ItemChangeQuantityView(GenericAPIView):
    serializer_class = serializers.ItemChangeQuantitySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.remote_user.id
        cart = models.Cart.objects.get(user_id=user_id)
        item = models.Item.objects.get(cart=cart, product_variant_id=serializer.data.get('product_variant_id'))
        item.quantity = serializer.data.get('quantity')
        item.save(update_fields=['quantity'])
        return Response({'item': item.id})


class ItemShowQuantityView(GenericAPIView):
    serializer_class = serializers.ItemShowQuantitySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.remote_user.id
        cart = models.Cart.objects.get(user_id=user_id)
        item = models.Item.objects.get(cart=cart, product_variant_id=serializer.data.get('product_variant_id'))
        return Response({'quantity': item.quantity})


class CartShowView(GenericAPIView):
    serializer_class = serializers.CartShowSerializer

    def get_queryset(self):
        handler = CartHandler(remote_user=self.request.remote_user)
        return handler.cart_show_queryset()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class CartCheckoutView(GenericAPIView):

    def get(self, request):
        cart = CartHandler(remote_user=request.remote_user)
        queryset = cart.cart_show_queryset()
        service = ProductsService(request=request, url=f"/api/v1/product/checkout/")
        response = service.service_response(
            method="post", json=list(queryset.values('id', 'product_variant_id', 'quantity'))
        )
        return Response(response.data)


class CartTotalView(GenericAPIView):
    serializer_class = serializers.CartTotalSerializer

    def get_queryset(self):
        handler = CartHandler(remote_user=self.request.remote_user)
        return handler.cart_total_queryset()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data[0])
