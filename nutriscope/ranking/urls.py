from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.my_ranking, name="mylist"),
    path('api/product-details/', views.get_product_details, name='get_product_details'),
]