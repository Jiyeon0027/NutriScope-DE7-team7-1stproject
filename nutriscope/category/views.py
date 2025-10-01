"""Category views"""

import json

from django.shortcuts import render
from common.models import NutriScopeData
import plotly.graph_objs as go
import plotly.utils


# 색상 팔레트
COLOR_PALETTE = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#FFEAA7",
    "#DDA0DD",
    "#98D8C8",
    "#F7DC6F",
    "#BB8FCE",
    "#85C1E9",
    "#F8C471",
    "#82E0AA",
    "#F1948A",
    "#85C1E9",
    "#D7BDE2",
    "#A9DFBF",
    "#F9E79F",
]


# 데이터 처리 함수들
def get_category_data():
    """카테고리별 상품 데이터를 가져오는 함수"""
    categories = [
        "프로틴",
        "유산균/프로바이오틱",
        "비타민",
        "홍삼/인삼",
        "마그네슘",
        "기타",
        "오메가3",
        "효소",
        "녹즙/주스",
        "꿀",
        "콜라겐",
        "기타 건강식품",
        "루테인",
        "비오틴",
        "아연",
        "칼슘",
        "밀크씨슬",
    ]

    data = {}
    for category in categories:
        data[category] = NutriScopeData.objects.filter(
            category=category
        ).order_by("rank")

    return data


def create_chart_data(data):
    """Plotly 차트를 생성하는 함수"""
    categories = list(data.keys())
    counts = [len(data[category]) for category in categories]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=counts,
                marker_color=COLOR_PALETTE,
            )
        ]
    )

    fig.update_layout(
        title="카테고리별 상품 수",
        xaxis_title="카테고리",
        yaxis_title="상품 수",
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=50, r=50, t=80, b=150),
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>상품 수 : %{y} <extra></extra>"
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_chart_pie_data(data):
    """Plotly 원형 차트를 생성하는 함수"""
    categories = list(data.keys())
    counts = [len(data[category]) for category in categories]

    # 전체 상품 수 계산
    total_count = sum(counts)

    # 퍼센트 계산 및 조건부 텍스트 설정
    text_labels = []
    for i, count in enumerate(counts):
        percentage = (count / total_count) * 100
        # 5% 이상인 경우만 라벨 표시
        if percentage >= 5:
            text_labels.append(categories[i])
        else:
            text_labels.append("")  # 작은 퍼센트는 빈 문자열

    fig = go.Figure(
        data=[
            go.Pie(
                labels=categories,
                values=counts,
                text=text_labels,  # 조건부 텍스트
                textinfo="text",  # 텍스트
                textposition="inside",
                hole=0.3,
                marker=dict(
                    colors=COLOR_PALETTE,
                ),
            )
        ]
    )

    fig.update_layout(
        title="카테고리별 상품 비율",
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=True,  # 범례 표시
        legend=dict(
            orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02
        ),
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>상품 수 : %{value}"
        + "<br>비율 : %{percent}<extra></extra>"
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def prepare_detailed_data(data):
    """상세 데이터를 JSON으로 변환하는 함수"""
    detailed_data = {}
    for category, products in data.items():
        detailed_data[category] = [
            {
                "product_name": product.product_name,
                "shop_name": product.shop_name,
                "brand_name": product.brand_name,
                "sale_price": product.sale_price,
                "rank": product.rank,
            }
            for product in products
        ]

    return json.dumps(detailed_data, ensure_ascii=False)


# 메인 뷰
def index(request):
    """카테고리 대시보드 메인 뷰"""
    # 데이터 가져오기
    data = get_category_data()

    # 차트 생성
    chart_json = create_chart_data(data)
    chart_pie_json = create_chart_pie_data(data)

    # 상세 데이터 준비
    detailed_data_json = prepare_detailed_data(data)

    # 템플릿에 전달할 컨텍스트
    context = {
        "title": "Category Summary",
        "data_items": data.items(),
        "chart": chart_json,
        "chart_pie": chart_pie_json,
        "detailed_data": detailed_data_json,
    }

    return render(request, "category/index.html", context)
