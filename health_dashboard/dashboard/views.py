# import pandas as pd
# import plotly.express as px
# from django.shortcuts import render

# # 데이터 불러오기
# df = pd.read_json('merged_products_top100_categorized.json')

# def index(request):
#     # 1. 가격 분포 히스토그램
#     fig_price_hist = px.histogram(df, x="sale_price", nbins=50, title="가격 분포 히스토그램")
#     price_hist_html = fig_price_hist.to_html(full_html=False)

#     # 2. 인기 브랜드 Top 10
#     top_n = 10
#     brand_counts = df['brand_name'].value_counts()
#     top_brands = brand_counts.head(top_n)
#     fig_brand_bar = px.bar(
#         top_brands,
#         x=top_brands.index,
#         y=top_brands.values,
#         title=f"Top {top_n} 인기 브랜드",
#         labels={"x": "브랜드", "y": "출현 횟수"},
#         text=top_brands.values
#     )
#     fig_brand_bar.update_traces(marker_color='skyblue', textposition='outside')
#     brand_bar_html = fig_brand_bar.to_html(full_html=False)

#     # 3. 카테고리별 상품수
#     category_counts = df['category'].value_counts()
#     fig_category_pie = px.pie(
#         names=category_counts.index,
#         values=category_counts.values,
#         title="카테고리별 비율"
#     )
#     category_pie_html = fig_category_pie.to_html(full_html=False)

#     context = {
#         "price_hist": price_hist_html,
#         "brand_bar": brand_bar_html,
#         "category_pie": category_pie_html
#     }
#     return render(request, "dashboard/index.html", context)


import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.shortcuts import render

def index(request):
    # 데이터 로드
    df = pd.read_json("merged_products_top100_categorized.json")

    # 가격 데이터 분포
    price_hist = px.histogram(df, x="sale_price", nbins=50, title="가격 분포 히스토그램")
    price_box = px.box(df, y="sale_price", points="all", title="가격 분포 박스플롯")

    # 인기 브랜드 Top N
    n = 10
    brand_counts = df["brand_name"].value_counts()
    top_brands = brand_counts.head(n)

    brand_bar = px.bar(
        top_brands,
        x=top_brands.index,
        y=top_brands.values,
        title=f"Top {n} 인기 브랜드",
        labels={"x": "브랜드", "y": "출현 횟수"},
        text=top_brands.values
    )
    brand_bar.update_traces(marker_color="skyblue", textposition="outside")
    brand_bar.update_layout(xaxis_tickangle=-45)

    brand_pie = px.pie(
        names=top_brands.index,
        values=top_brands.values,
        title=f"Top {n} 인기 브랜드 비율"
    )

    brand_tree = px.treemap(
        names=top_brands.index,
        parents=[""] * n,
        values=top_brands.values,
        title=f"Top {n} 인기 브랜드 트리맵"
    )

    # 카테고리별 상품 수
    category_counts = df["category"].value_counts()

    category_bar = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="카테고리별 데이터 개수",
        labels={"x": "카테고리", "y": "개수"},
        text=category_counts.values
    )
    category_bar.update_traces(marker_color="skyblue", textposition="outside")

    category_pie = px.pie(
        names=category_counts.index,
        values=category_counts.values,
        title="카테고리별 비율"
    )

    category_tree = px.treemap(
        names=category_counts.index,
        parents=[""] * len(category_counts),
        values=category_counts.values,
        title="카테고리별 트리맵"
    )

    # Plotly → HTML 변환
    context = {
        "price_hist": pio.to_html(price_hist, full_html=False),
        "price_box": pio.to_html(price_box, full_html=False),
        "brand_bar": pio.to_html(brand_bar, full_html=False),
        "brand_pie": pio.to_html(brand_pie, full_html=False),
        "brand_tree": pio.to_html(brand_tree, full_html=False),
        "category_bar": pio.to_html(category_bar, full_html=False),
        "category_pie": pio.to_html(category_pie, full_html=False),
        "category_tree": pio.to_html(category_tree, full_html=False),
    }
    return render(request, "dashboard/index.html", context)
