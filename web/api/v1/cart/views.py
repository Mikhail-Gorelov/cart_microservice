import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from cart import models
from . import serializers

logger = logging.getLogger(__name__)


# Create your views here.

class CartAddView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user_id = self.request.user.pk
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
        user_id = self.request.user.pk
        cart = models.Cart.objects.get(user_id=user_id)
        models.Item.objects.create(cart=cart, **serializer.data)
        return Response(serializer.data)


class CartShowView(GenericAPIView):
    serializer_class = serializers.CartShowSerializer

    def get_queryset(self):
        user_id = self.request.user.pk
        return models.Item.objects.filter(cart__user_id=user_id) if user_id else models.Item.objects.filter(
            cart__session_id=user_id)
