# load_data.py
import os
import django
import json

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nutriscope.settings")  # ⚠️ settings.py 경로 확인!
django.setup()

from dashboard.models import Product

# JSON 파일 읽기
with open("merged_products_top100_preprocessed_fin.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 데이터 적재
for item in data:
    # 문자열 필드 기본값 처리
    shop_name = item.get("shop_name") or "없음"
    display_name = item.get("display_name") or "없음"
    product_name = item.get("product_name") or "없음"
    quantity = item.get("quantity") or "없음"
    brand_name = item.get("brand_name") or "없음"
    image_url = item.get("image_url") or ""

    category = item.get("category") or "기타"

    # 정수/숫자 필드 기본값 처리
    original_price = item.get("original_price")
    if original_price in [None, ""]:
        original_price = 0

    sale_price = item.get("sale_price")
    if sale_price in [None, ""]:
        sale_price = 0

    rank = item.get("rank")
    if rank in [None, ""]:
        rank = 0

    # DB에 저장
    Product.objects.create(
        shop_name=shop_name,
        display_name=display_name,
        product_name=product_name,
        quantity=quantity,
        brand_name=brand_name,
        original_price=original_price,
        sale_price=sale_price,
        image_url=image_url,
        rank=rank,
        category=category,
    )

print("✅ JSON 데이터를 DB에 안전하게 적재 완료!")
