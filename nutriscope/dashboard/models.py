"""dashboard 모델"""

from common.models import NutriScopeData


class Product(NutriScopeData):
    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.product_name} ({self.brand_name})"
