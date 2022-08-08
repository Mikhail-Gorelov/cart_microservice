from microservice_request.services import ConnectionService
from django.conf import settings
from main.services import RemoteUser
from order.choices import OrderStatus
from order.models import Order, OrderLine


class OrderHandler:
    def __init__(self, *, remote_user: RemoteUser):
        self.remote_user = remote_user

    def add_to_order(self, product_variant_id: int, quantity: int) -> OrderLine:
        order = self._get_or_create_order()
        # product_variant_id, product_name, variant_name, product_sku - в вариант uuid64, quantity - из item, currency из channel, api_gateway
        # service = ProductServiceRequest(url='api/v1/sign-in/email/')
        # response = service.service_response(method="post", data=serializer.data)
        return OrderLine.objects.get_or_create(order=order, product_variant_id=product_variant_id, quantity=quantity)

    def _get_or_create_order(self) -> Order:
        return Order.objects.get_or_create(user_id=self.remote_user.id, status=OrderStatus.DRAFT)


class ProductServiceRequest(ConnectionService):
    api_key = settings.PRODUCTS_API_KEY
    service = settings.PRODUCTS_API_URL
