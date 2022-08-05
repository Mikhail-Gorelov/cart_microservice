from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.order import views

app_name = 'cart'

router = DefaultRouter()

urlpatterns = [
    path('item/add/', views.ItemAddView.as_view(), name='item-add'),
]

urlpatterns += router.urls
