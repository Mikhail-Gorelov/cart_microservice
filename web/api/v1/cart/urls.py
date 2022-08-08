from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.cart import views

app_name = 'cart'

router = DefaultRouter()

urlpatterns = [
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('item/add/', views.ItemAddView.as_view(), name='item-add'),
    path('cart/show/', views.CartShowView.as_view(), name='cart-show')
]

urlpatterns += router.urls
