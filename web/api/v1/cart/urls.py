from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.cart import views

app_name = 'cart'

router = DefaultRouter()

urlpatterns = [
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
]

urlpatterns += router.urls
