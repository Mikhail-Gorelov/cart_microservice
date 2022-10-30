from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.order import views

app_name = 'order'

router = DefaultRouter()

urlpatterns = [
    path('item-order/add/', views.ItemOrderAddView.as_view(), name='item-order-add'),
    path('item-order/show/draft/', views.ItemOrderShowDraftView.as_view(), name='item-order-show-draft'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
]

urlpatterns += router.urls
