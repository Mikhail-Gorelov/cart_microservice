import logging

from oauthlib.common import urldecode
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers
from order.models import Order
from order import choices
from .services import OrderHandler

logger = logging.getLogger(__name__)


# Create your views here.


class ItemOrderAddView(GenericAPIView):
    serializer_class = serializers.ItemOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handler = OrderHandler(remote_user=self.request.remote_user)
        reg_country = dict(urldecode(request.COOKIES.get('reg_country')))
        handler.add_to_order(product_variant_id=serializer.data['product_variant_id'],
                             quantity=serializer.data['quantity'],
                             currency=reg_country.get('currency_code'))
        return Response(serializer.data)


class ItemOrderShowDraftView(GenericAPIView):
    serializer_class = serializers.DraftOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(status=choices.OrderStatus.DRAFT)

    def get(self, request):
        instance = self.get_queryset().get(user_id=self.request.remote_user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CheckoutView(GenericAPIView):
    pass
