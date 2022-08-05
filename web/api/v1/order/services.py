from order.models import Order, OrderLine


class OrderHandler:
    def __init__(self, *, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id

    def add_to_order(self, product_variant_id: int, quantity: int) -> OrderLine:
        order = self._get_or_create_order()
        return OrderLine.objects.get_or_create(order=order, product_variant_id=product_variant_id, quantity=quantity)

    def _get_or_create_order(self) -> Order:
        return Order.objects.get_or_create(user_id=self.user_id)
