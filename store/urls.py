from django.urls import path
from . import views

urlpatterns = [
    path('', views.stores, name='store'),
    path('category/<slug:category_slug>/',
         views.stores, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
]
