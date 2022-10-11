from django.conf import settings
from microservice_request.services import MicroServiceConnect

from cart import models
from main.services import RemoteUser


class CartHandler:
    def __init__(self, *, remote_user: RemoteUser):
        self.remote_user = remote_user

    def cart_show_queryset(self):
        user_id = self.remote_user.id
        if user_id:
            return models.Item.objects.filter(cart__user_id=user_id)
        return models.Item.objects.filter(cart__session_id=user_id)


class ProductsService(MicroServiceConnect):
    api_key = settings.PRODUCTS_API_KEY
    service = settings.PRODUCTS_API_URL
