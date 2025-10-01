# dashboard/load_data.py
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthdashboard_claude.settings")
django.setup()

from dashboard.models import Product

with open('merged_products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    Product.objects.create(
        shop_name=item.get("shop_name", ""),
        display_name=item.get("display_name", ""),
        product_name=item.get("product_name", ""),
        quantity=item.get("quantity", ""),
        brand_name=item.get("brand_name", ""),
        original_price=item.get("original_price", 0),
        sale_price=item.get("sale_price", 0),
        image_url=item.get("image_url", ""),
        rank=item.get("rank", 0),
        category=item.get("category", "")
    )

print("✅ 데이터 적재 완료!")
