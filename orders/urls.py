from django.urls import path, include
from . import views

urlpatterns = [
    path('order_complete/', views.order_complete, name='order_complete'),
]
