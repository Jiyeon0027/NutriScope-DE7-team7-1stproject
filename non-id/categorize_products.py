#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from collections import defaultdict, Counter
import os


def load_json_files():
    """모든 JSON 파일을 로드합니다."""
    json_files = [
        "data.json",
        "gmarket_product_list_20250929_1.json",
        "kakao_gift_products.json",
        "kurly_products_int.json",
    ]

    all_products = []

    for file_name in json_files:
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_products.extend(data)
                    print(
                        f"✅ {file_name}: {len(data) if isinstance(data, list) else 1}개 제품 로드"
                    )
            except Exception as e:
                print(f"❌ {file_name} 로드 실패: {e}")
        else:
            print(f"⚠️ {file_name} 파일을 찾을 수 없습니다.")

    return all_products


def categorize_product(display_name):
    """display_name을 기반으로 제품을 카테고리화합니다."""
    display_name = display_name.lower()

    # 카테고리 키워드 매핑
    categories = {
        "비타민": [
            "비타민",
            "vitamin",
            "멀티비타민",
            "이뮨",
            "비타민c",
            "비타민d",
            "비타민b",
            "비타민e",
            "비타민a",
        ],
        "홍삼/인삼": [
            "홍삼",
            "인삼",
            "홍삼정",
            "홍삼진",
            "산삼",
            "6년근",
            "홍삼스틱",
            "홍삼앰플",
            "홍삼액",
        ],
        "오메가3": [
            "오메가3",
            "오메가",
            "omega",
            "피쉬오일",
            "알티지",
            "dha",
            "epa",
            "rTG",
        ],
        "유산균/프로바이오틱": [
            "유산균",
            "프로바이오틱",
            "락토핏",
            "lacto",
            "probiotic",
            "생유산균",
        ],
        "콜라겐": ["콜라겐", "collagen", "가수분해", "콜라겐펩타이드"],
        "마그네슘": ["마그네슘", "magnesium", "mg"],
        "칼슘": ["칼슘", "calcium", "ca"],
        "아연": ["아연", "zinc", "zn"],
        "밀크씨슬": ["밀크씨슬", "milk thistle", "실리마린"],
        "루테인": ["루테인", "lutein", "눈건강"],
        "비오틴": ["비오틴", "biotin"],
        "프로틴": ["프로틴", "protein", "단백질", "쉐이크"],
        "효소": ["효소", "enzyme", "브랜드밀효소"],
        "녹즙/주스": ["녹즙", "주스", "juice", "케일", "사과", "매실", "원액"],
        "꿀": ["꿀", "honey", "벌꿀", "아카시아", "야생화"],
        "기타 건강식품": [
            "침향",
            "침향환",
            "침향단",
            "도라지",
            "배도라지",
            "프로폴리스",
            "매실",
        ],
    }

    # 카테고리 매칭
    matched_categories = []
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in display_name:
                matched_categories.append(category)
                break

    # 매칭된 카테고리가 없으면 '기타'로 분류
    if not matched_categories:
        return "기타"

    # 여러 카테고리가 매칭되면 첫 번째 카테고리 반환
    return matched_categories[0]


def analyze_categories(all_products):
    """제품들을 카테고리별로 분석합니다."""
    category_stats = defaultdict(list)
    category_counts = Counter()

    for product in all_products:
        if "display_name" in product:
            display_name = product["display_name"]
            category = categorize_product(display_name)

            # 제품 정보에 카테고리 추가
            product["category"] = category

            # 카테고리별 통계
            category_stats[category].append(product)
            category_counts[category] += 1

    return category_stats, category_counts


def print_category_analysis(category_counts, category_stats):
    """카테고리 분석 결과를 출력합니다."""
    print("\n" + "=" * 80)
    print("📊 제품 카테고리 분석 결과")
    print("=" * 80)

    # 카테고리별 개수 출력
    print("\n📈 카테고리별 제품 개수:")
    for category, count in category_counts.most_common():
        print(f"  {category}: {count}개")

    print(f"\n총 제품 수: {sum(category_counts.values())}개")
    print(f"총 카테고리 수: {len(category_counts)}개")

    # 각 카테고리별 상세 정보
    print("\n" + "=" * 80)
    print("📋 카테고리별 상세 정보")
    print("=" * 80)

    for category in sorted(category_counts.keys()):
        products = category_stats[category]
        print(f"\n🔸 {category} ({len(products)}개)")
        print("-" * 50)

        # 샘플 제품 3개 출력
        for i, product in enumerate(products[:3]):
            shop = product.get("shop_name", "Unknown")
            name = (
                product.get("display_name", "Unknown")[:60] + "..."
                if len(product.get("display_name", "")) > 60
                else product.get("display_name", "Unknown")
            )
            print(f"  {i+1}. [{shop}] {name}")

        if len(products) > 3:
            print(f"  ... 외 {len(products)-3}개")


def save_categorized_data(category_stats):
    """카테고리별로 분류된 데이터를 저장합니다."""
    # 전체 카테고리별 데이터 저장
    with open("categorized_products.json", "w", encoding="utf-8") as f:
        json.dump(dict(category_stats), f, ensure_ascii=False, indent=2)

    # 각 카테고리별 개별 파일 저장
    for category, products in category_stats.items():
        # 파일명에 사용할 수 없는 문자 제거
        safe_category = re.sub(r"[^\w\s-]", "", category).strip()
        safe_category = re.sub(r"[-\s]+", "_", safe_category)

        filename = f"category_{safe_category}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\n💾 카테고리별 데이터가 저장되었습니다:")
    print(f"  - categorized_products.json (전체)")
    print(f"  - category_*.json (카테고리별 개별 파일)")


def main():
    """메인 함수"""
    print("🚀 제품 카테고리 분석을 시작합니다...")

    # JSON 파일들 로드
    all_products = load_json_files()

    if not all_products:
        print("❌ 로드된 제품이 없습니다.")
        return

    print(f"\n📦 총 {len(all_products)}개 제품을 분석합니다.")

    # 카테고리 분석
    category_stats, category_counts = analyze_categories(all_products)

    # 결과 출력
    print_category_analysis(category_counts, category_stats)

    # 데이터 저장
    save_categorized_data(category_stats)

    print("\n✅ 카테고리 분석이 완료되었습니다!")


if __name__ == "__main__":
    main()
