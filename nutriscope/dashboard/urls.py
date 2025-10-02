from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('product-comparison/', views.product_comparison, name='product_comparison'),
    # Product 목록 API
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('compare-table/', views.compare_table, name = 'compare_table'),
    path('product-list/', views.base_view, name='base'),  # 여기 추가
    # path('category-price/', views.category_price_view, name='category_price'),
    # path('get_treemap_data/', views.get_treemap_data, name='get_treemap_data'),
    # path('get_barchart_data/<str:category>/', views.get_barchart_data, name='get_barchart_data'),
        # 카테고리-가격 분석 페이지
    # 카테고리-가격 분석 페이지
    path('category-price/', views.category_price_view, name='category_price'),
    
    # API 엔드포인트
    path('api/get_treemap_data/', views.get_treemap_data, name='get_treemap_data'),
    path('api/get_barchart_data/', views.get_barchart_data, name='get_barchart_data'),
]