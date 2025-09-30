import json
import re
from collections import defaultdict, Counter


def categorize_product(display_name):
    """display_name을 기반으로 제품을 카테고리화합니다."""
    display_name = display_name.lower()

    # 카테고리 키워드 매핑 (non-id 폴더의 분류 로직과 동일)
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


def categorize_merged_products():
    """merged_products_top100.json 파일의 제품들을 카테고리별로 분류합니다."""
    print(
        "🚀 merged_products_top100.json 파일의 제품 카테고리 분류를 시작합니다..."
    )

    # JSON 파일 로드
    try:
        with open("merged_products_top100.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        print(f"✅ merged_products_top100.json: {len(products)}개 제품 로드")
    except Exception as e:
        print(f"❌ merged_products_top100.json 로드 실패: {e}")
        return

    # 카테고리 분석
    category_stats = defaultdict(list)
    category_counts = Counter()

    for product in products:
        if "display_name" in product:
            display_name = product["display_name"]
            category = categorize_product(display_name)

            # 제품 정보에 카테고리 추가
            product["category"] = category

            # 카테고리별 통계
            category_stats[category].append(product)
            category_counts[category] += 1

    # 결과 출력
    print("\n" + "=" * 80)
    print("📊 제품 카테고리 분석 결과")
    print("=" * 80)

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
        products_in_category = category_stats[category]
        print(f"\n🔸 {category} ({len(products_in_category)}개)")
        print("-" * 50)

        # 샘플 제품 3개 출력
        for i, product in enumerate(products_in_category[:3]):
            shop = product.get("shop_name", "Unknown")
            name = (
                product.get("display_name", "Unknown")[:60] + "..."
                if len(product.get("display_name", "")) > 60
                else product.get("display_name", "Unknown")
            )
            print(f"  {i+1}. [{shop}] {name}")

        if len(products_in_category) > 3:
            print(f"  ... 외 {len(products_in_category)-3}개")

    # 카테고리가 추가된 제품 데이터 저장
    with open(
        "merged_products_top100_categorized.json", "w", encoding="utf-8"
    ) as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    # 카테고리별 개별 파일 저장
    for category, products_in_category in category_stats.items():
        # 파일명에 사용할 수 없는 문자 제거
        safe_category = re.sub(r"[^\w\s-]", "", category).strip()
        safe_category = re.sub(r"[-\s]+", "_", safe_category)

        filename = f"merged_category_{safe_category}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products_in_category, f, ensure_ascii=False, indent=2)

    print(f"\n💾 카테고리별 데이터가 저장되었습니다:")
    print(f"  - merged_products_top100_categorized.json (전체)")
    print(f"  - merged_category_*.json (카테고리별 개별 파일)")

    print("\n✅ 카테고리 분류가 완료되었습니다!")


if __name__ == "__main__":
    categorize_merged_products()
