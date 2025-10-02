from django.urls import path
from .views import *

urlpatterns = [
    path("detail/", FamousBrandDetailView.as_view(), name="brand_detail")
]
