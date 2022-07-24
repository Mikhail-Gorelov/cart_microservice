import logging

from rest_framework.permissions import AllowAny

from . import serializers
from cart import models
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


# Create your views here.

class CartAddView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user.pk
        else:
            user = self.request.headers.get('Remote-User')

        try:
            obj = models.Cart.objects.get(user_id=user)
        except models.Cart.DoesNotExist:
            obj = models.Cart(user_id=user)
            obj.save()
        return Response({'cart_id': obj.pk})


class ItemAddView(GenericAPIView):
    serializer_class = serializers.ItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_authenticated:
            user = self.request.user.pk
        else:
            user = self.request.headers.get('Remote-User')

        cart = models.Cart.objects.get(user_id=user)
        models.Item.objects.create(cart=cart, **serializer.data)
        return Response(serializer.data)

class CartShowView(GenericAPIView):
    serializer_class = serializers.CartShowSerializer

    def get_queryset(self):
        user_id: int | None = self.request.user.pk if self.request.user.is_authenticated else self.request.headers.get('Remote-User')

        if user_id:
            return models.Item.objects.filter(cart__user_id=user_id)
        else:
            # self.request.session
            return models.Item.objects.filter(cart__session_id=user_id)
