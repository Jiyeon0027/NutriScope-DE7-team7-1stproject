from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('product-comparison/', views.product_comparison, name='product_comparison'),
    # Product 목록 API
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('compare-table/', views.compare_table, name = 'compare_table'),
    path('product-list/', views.base_view, name='base'),  # 여기 추가
]