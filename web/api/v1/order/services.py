from microservice_request.services import ConnectionService
from django.conf import settings
from main.services import RemoteUser
from order.choices import OrderStatus
from order.models import Order, OrderLine, OrderLineData


class OrderHandler:
    def __init__(self, *, remote_user: RemoteUser):
        self.remote_user = remote_user

    def add_to_order(self, product_variant_id: int, quantity: int, currency: str) -> OrderLine:
        if not currency:
            currency = ''
        order = self._get_or_create_order()
        service = ProductServiceRequest(url=f'/api/v1/product-variant/{product_variant_id}/')
        response = service.service_response(method="get")
        orderline_data = OrderLineData(
            order=order[0],
            product_variant_id=product_variant_id,
            product_name=response.data['product_name'],
            variant_name=response.data['variant_name'],
            product_sku=response.data['product_sku'],
            quantity=quantity,
            currency=currency
        )
        return OrderLine.objects.get_or_create(**orderline_data._asdict())

    def _get_or_create_order(self) -> tuple[Order, bool]:
        return Order.objects.get_or_create(user_id=self.remote_user.id, status=OrderStatus.DRAFT, channel_id=1)


class ProductServiceRequest(ConnectionService):
    api_key = settings.PRODUCTS_API_KEY
    service = settings.PRODUCTS_API_URL
