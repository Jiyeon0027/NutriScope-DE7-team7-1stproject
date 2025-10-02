"""카테고리 모델"""

from common.models import NutriScopeData


class CategoryData(NutriScopeData):
    """카테고리에서 사용할 메서드 정의"""

    class Meta:
        proxy = True

    def __str__(self):
        return (
            f"{self.category} - {self.representative_name} - {self.total_rank}"
        )

    @classmethod
    def get_available_categories(cls):
        """데이터베이스에서 실제 존재하는 카테고리들을 가져옴"""
        return cls.objects.values_list("category", flat=True).distinct()

    @classmethod
    def get_category_data(cls):
        """카테고리별 상품 데이터를 가져오는 클래스 메서드"""
        categories = cls.get_available_categories()

        data = {}
        for category in categories:
            data[category] = cls.objects.filter(category=category).order_by(
                "rank"
            )

        return data
