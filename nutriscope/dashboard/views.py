from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import plotly
import json
import os
from django.db import models
from django.conf import settings
from dashboard.models import Product
from django.http import JsonResponse
from django.db.models import Avg, Count
from famous_brand.controllers import *
queryset = Product.objects.all().values()
df = pd.DataFrame(list(queryset))
def dashboard_view(request):
    # JSON 파일 경로 설정
    # json_path = os.path.join(settings.BASE_DIR, 'merged_products_top100_categorized.json')
    # queryset = Product.objects.all().values()
    # df = pd.DataFrame(list(queryset))
    # 데이터 로드
    #df = pd.read_json(json_path)
    
    # print("=== 데이터 확인 ===")
    # print(f"전체 행 수: {len(df)}")
    # print(f"컬럼: {df.columns.tolist()}")
    # print(f"브랜드 샘플: {df['brand_name'].head()}")
    
    # 1. 가격 분포 히스토그램
    fig_histogram = go.Figure(data=[
        go.Histogram(
            x=df['sale_price'].tolist(),
            nbinsx=50,
            marker_color='#0064FF'
        )
    ])
    fig_histogram.update_layout(
        title="가격 분포",
        xaxis_title="가격 (원)",
        yaxis_title="제품 수",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=60, l=60, r=40)
    )
    
    # 2. 가격 분포 박스플롯
    fig_box = go.Figure(data=[
        go.Box(
            y=df['sale_price'].tolist(),
            marker_color='#0064FF',
            name='가격'
        )
    ])
    fig_box.update_layout(
        title="가격 분포 상세",
        yaxis_title="가격 (원)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=60, l=60, r=40),
        showlegend=False
    )
    
    # 3. 인기 브랜드 Top 10

    brand_name = request.GET.get("brand_name", "brand_name") # query가 있을경우 "brand_name"을 인자로 받는다. 없을경우 "brand_name"을 default로 리턴
    brand_graph_bar = Brand(brand_name).draw_top_chart('bar')
    brand_graph_pie = Brand(brand_name).draw_top_chart('pie')

    '''
    n = 10
    brand_counts = df['brand_name'].value_counts()
    top_brands = brand_counts.head(n)
    
    print(f"\n=== Top {n} 브랜드 ===")
    print(top_brands)
    
    # 브랜드 막대 그래프
    fig_brand_bar = go.Figure(data=[
        go.Bar(
            x=top_brands.index.tolist(),
            y=top_brands.values.tolist(),
            text=top_brands.values.tolist(),
            textposition='outside',
            marker_color='#0064FF'
        )
    ])
    fig_brand_bar.update_layout(
        title=f"Top {n} 인기 브랜드",
        xaxis_title="브랜드",
        yaxis_title="제품 수",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        xaxis_tickangle=-45,
        margin=dict(t=60, b=100, l=60, r=40)
    )
    
    # 브랜드 파이차트
    fig_brand_pie = go.Figure(data=[
        go.Pie(
            labels=top_brands.index.tolist(),
            values=top_brands.values.tolist(),
            hole = 0.4
        )
    ])
    fig_brand_pie.update_layout(
        title=f"Top {n} 브랜드 비율",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    '''
    
    # 4. 카테고리별 상품 수
    category_counts = df['category'].value_counts()
    
    # print(f"\n=== 카테고리 ===")
    # print(category_counts)
    
    # 카테고리 막대 그래프
    fig_category_bar = go.Figure(data=[
        go.Bar(
            x=category_counts.index.tolist(),
            y=category_counts.values.tolist(),
            text=category_counts.values.tolist(),
            textposition='outside',
            marker_color='#00C8B5'
        )
    ])
    fig_category_bar.update_layout(
        title="카테고리별 제품 수",
        xaxis_title="카테고리",
        yaxis_title="제품 수",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=60, l=60, r=40)
    )
    
    # 카테고리 트리맵
    fig_category_tree = go.Figure(data=[
        go.Treemap(
            labels=category_counts.index.tolist(),
            parents=[""]*len(category_counts),
            values=category_counts.values.tolist(),
            textposition='middle center'
        )
    ])
    fig_category_tree.update_layout(
        title="카테고리 트리맵",
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    # 통계 데이터
    stats = {
        'total_products': len(df),
        'avg_price': int(df['sale_price'].mean()),
        'total_brands': df['brand_name'].nunique(),
        'total_categories': df['category'].nunique(),
    }
    
    # print(f"\n=== 통계 ===")
    # print(stats)
    
    # JSON으로 변환 (safe하게)
    context = {
        'histogram_json': json.dumps(fig_histogram.to_dict()),
        'box_json': json.dumps(fig_box.to_dict()),
        'brand_bar_json': json.dumps(brand_graph_bar.to_dict()),
        'brand_pie_json': json.dumps(brand_graph_pie.to_dict()),
        'category_bar_json': json.dumps(fig_category_bar.to_dict()),
        'category_tree_json': json.dumps(fig_category_tree.to_dict()),
        'stats': stats,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

#################################  product_comparison ##################################
def product_comparison(request):
    # 필요한 context 데이터 추가 가능
    context = {}
    return render(request, 'dashboard/product_comparison.html', context)

# def product_list_api(request):
    # id 순으로 정렬
    # products = list(Product.objects.all().order_by('id').values('id', 'shop_name', 'product_name', 'brand_name','sale_price', 'image_url', 'quantity'))
    # return JsonResponse(products, safe=False)

def product_list_api(request):
    products = list(Product.objects.all().order_by('id').values(
        'id', 'shop_name', 'product_name', 'brand_name',
        'sale_price', 'image_url', 'quantity', 'category'  # ← category 추가!
    ))
    return JsonResponse(products, safe=False)

#################################  compare table  ##################################
def compare_table(request):
    brand = request.GET.get('brand', '').strip()
    product_name = request.GET.get('product_name', '').strip()
    shop_name = request.GET.get('shop_name', '').strip()

    products = Product.objects.all()

    if brand:
        products = products.filter(brand_name__icontains=brand)
    if product_name:
        products = products.filter(product_name__icontains=product_name)
    if shop_name:
        products = products.filter(shop_name__icontains=shop_name)

    products = products.order_by('sale_price')  # 가격순 정렬

    return render(request, 'dashboard/compare_table.html', {
        'products': products,
        'brand': brand,
        'product_name': product_name,
        'shop_name': shop_name,
    })
################################# base_view  ########################################
# def base_view(request):
#     return render(request, 'dashboard/base.html')
def base_view(request):
    keyword = request.GET.get('keyword', '').strip().lower()
    sort_option = request.GET.get('sort', 'id-asc')

    products = Product.objects.all()

    # 검색
    if keyword:
        products = products.filter(
            product_name__icontains=keyword
        ) | products.filter(
            brand_name__icontains=keyword
        ) | products.filter(
            shop_name__icontains=keyword
        )

    # 정렬
    if sort_option == 'id-asc':
        products = products.order_by('id')
    elif sort_option == 'id-desc':
        products = products.order_by('-id')
    elif sort_option == 'price-asc':
        products = products.order_by('sale_price')
    elif sort_option == 'price-desc':
        products = products.order_by('-sale_price')

    # 통계
    total_products = products.count()
    avg_price = int(products.aggregate(avg_price=Avg('sale_price'))['avg_price'] or 0)
    total_brands = products.values('brand_name').distinct().count()
    total_categories = products.values('category').distinct().count()

    # 쇼핑몰별 제품 수 pie chart
    shop_counts = products.values('shop_name').annotate(count=Count('id'))
    if shop_counts:
        fig = px.pie(
            names=[x['shop_name'] for x in shop_counts],
            values=[x['count'] for x in shop_counts],
            title="쇼핑몰별 제품 비율"
        )
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph_json = None

    context = {
        'products': products[:5],
        'stats': {
            'total_products': total_products,
            'avg_price': avg_price,
            'total_brands': total_brands,
            'total_categories': total_categories,
        },
        'graph_json': graph_json,
        'keyword': keyword,
        'sort_option': sort_option
    }

    return render(request, 'dashboard/base.html', context)

############################ d3 dashboard #######################################
def category_price_view(request):
    """카테고리-가격 분석 페이지"""
    return render(request, "dashboard/category_price.html")

def get_treemap_data(request):
    """트리맵 데이터: 카테고리별 제품 수"""
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    
    treemap_data = []
    for _, row in category_counts.iterrows():
        treemap_data.append({
            "category": row['category'],
            "value": int(row['count'])
        })
    
    return JsonResponse(treemap_data, safe=False)

def get_barchart_data(request):  # category 파라미터 제거
    """바차트 데이터: 가격대별 제품 수"""
    # GET 쿼리 파라미터로 카테고리 받기
    category = request.GET.get('category', 'All')
    
    # 카테고리 필터링
    if category == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[df['category'] == category].copy()
    
    # 가격대 구간 설정
    bins = [0, 15000, 25900, 41700, float('inf')]
    labels = ["저가", "중저가", "중고가", "고가"]
    
    # 가격대 그룹화
    filtered_df['price_range'] = pd.cut(
        filtered_df['sale_price'], 
        bins=bins, 
        labels=labels, 
        right=True
    )
    
    # 각 가격대별 카운트
    price_counts = filtered_df['price_range'].value_counts().sort_index()
    
    # 모든 가격대가 포함되도록 보장
    barchart_data = []
    for label in labels:
        count = price_counts.get(label, 0)
        barchart_data.append({
            "category": label,
            "value": int(count),
            "group": category
        })
    
    return JsonResponse(barchart_data, safe=False)
