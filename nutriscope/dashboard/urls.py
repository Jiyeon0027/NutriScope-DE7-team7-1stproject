from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('product-comparison/', views.product_comparison, name='product_comparison'),
    # Product 목록 API
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('compare-table/', views.compare_table, name = 'compare_table'),
    path('product-list/', views.base_view, name='base'),  # 여기 추가
    # 카테고리-가격 분석 페이지
    path('category-price/', views.category_price_view, name='category_price'),
    
    # API 엔드포인트
    path('api/get_treemap_data/', views.get_treemap_data, name='get_treemap_data'),
    path('api/get_barchart_data/', views.get_barchart_data, name='get_barchart_data'),
    path('famous_brand/', include('famous_brand.urls')), # famous_brand App에 대한 url 경로 설정
    path('ranking/', include('ranking.urls')),  # 랭킹 앱
    path('category/', include('category.urls')), # category 앱
        
]