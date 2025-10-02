from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from django.core.paginator import Paginator
from common.models import NutriScopeData

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def my_ranking(request):
    data = (
        NutriScopeData.objects
        .values("representative_name", "category")  # 그룹핑 기준
        .annotate(rank=Max("total_rank"))  # 같은 representative_name 안에서 가장 높은 total_rank
        .order_by("rank")  # 오름차순 정렬
    )
    # 페이지네이션
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "ranking/my_ranking.html", {"page_obj": page_obj})

def get_product_details(request):
    """AJAX로 제품 상세 정보를 반환하는 뷰"""
    representative_name = request.GET.get('representative_name')
    
    if not representative_name:
        return JsonResponse({'error': '제품명이 제공되지 않았습니다.'}, status=400)
    
    # 해당 representative_name을 가진 모든 제품 조회
    products = NutriScopeData.objects.filter(
        representative_name=representative_name
    ).values(
        'image_url',
        'shop_name', 
        'brand_name',
        'display_name',
        'product_name',
        'original_price',
        'sale_price',
        'quantity'
    )
    
    products_list = list(products)
    
    return JsonResponse({
        'representative_name': representative_name,
        'products': products_list
    })

