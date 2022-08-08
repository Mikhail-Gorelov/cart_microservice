import logging

from rest_framework.permissions import AllowAny

from . import serializers
from cart import models
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .services import OrderHandler

logger = logging.getLogger(__name__)


# Create your views here.


class ItemAddView(GenericAPIView):
    serializer_class = serializers.ItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handler = OrderHandler(remote_user=request.remote_user)
        handler.add_to_order(product_variant_id=serializer.data['product_variant_id'],
                             quantity=serializer.data['quantity'])
        return Response(serializer.data)
