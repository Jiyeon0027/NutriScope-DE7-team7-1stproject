from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from django.conf import settings

def dashboard_view(request):
    # JSON 파일 경로 설정
    json_path = os.path.join(settings.BASE_DIR, 'merged_products_top100_categorized.json')
    
    # 데이터 로드
    df = pd.read_json(json_path)
    
    print("=== 데이터 확인 ===")
    print(f"전체 행 수: {len(df)}")
    print(f"컬럼: {df.columns.tolist()}")
    print(f"브랜드 샘플: {df['brand_name'].head()}")
    
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
            values=top_brands.values.tolist()
        )
    ])
    fig_brand_pie.update_layout(
        title=f"Top {n} 브랜드 비율",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Pretendard, sans-serif"),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    
    # 4. 카테고리별 상품 수
    category_counts = df['category'].value_counts()
    
    print(f"\n=== 카테고리 ===")
    print(category_counts)
    
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
    
    print(f"\n=== 통계 ===")
    print(stats)
    
    # JSON으로 변환 (safe하게)
    context = {
        'histogram_json': json.dumps(fig_histogram.to_dict()),
        'box_json': json.dumps(fig_box.to_dict()),
        'brand_bar_json': json.dumps(fig_brand_bar.to_dict()),
        'brand_pie_json': json.dumps(fig_brand_pie.to_dict()),
        'category_bar_json': json.dumps(fig_category_bar.to_dict()),
        'category_tree_json': json.dumps(fig_category_tree.to_dict()),
        'stats': stats,
    }
    
    return render(request, 'dashboard/dashboard.html', context)