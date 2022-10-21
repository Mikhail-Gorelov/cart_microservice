from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.cart import views

app_name = 'cart'

router = DefaultRouter()

urlpatterns = [
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('item/add/', views.ItemAddView.as_view(), name='item-add'),
    path('item/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    path('item/change-quantity/', views.ItemChangeQuantityView.as_view(), name='item-change-quantity'),
    path('item/show-quantity/', views.ItemShowQuantityView.as_view(), name='item-show-quantity'),
    path('cart/show/', views.CartShowView.as_view(), name='cart-show'),
    path('cart/checkout/', views.CartCheckoutView.as_view(), name='cart-checkout'),
    path('cart/total/', views.CartTotalView.as_view(), name='cart-total'),
]

urlpatterns += router.urls
