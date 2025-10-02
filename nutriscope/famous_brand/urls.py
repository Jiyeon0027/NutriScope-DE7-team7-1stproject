from django.urls import path
from .views import *

urlpatterns = [
    path('', FamousBrandView.as_view(), name="top_famousbrand"),
    path("detail/", FamousBrandDetailView.as_view(), name="brand_detail")
]
