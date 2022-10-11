import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from cart import models
from . import serializers
from .services import CartHandler

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


class CartShowView(GenericAPIView):
    serializer_class = serializers.CartShowSerializer

    def get_queryset(self):
        handler = CartHandler(remote_user=self.request.remote_user)
        return handler.cart_show_queryset()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class CartTotalView(GenericAPIView):
    serializer_class = serializers.CartTotalSerializer

    def get_queryset(self):
        handler = CartHandler(remote_user=self.request.remote_user)
        return handler.cart_total_queryset()

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
