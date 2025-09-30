"""공통 모델"""

from django.db import models


# Create your models here.
class NutriScopeData(models.Model):
    """공통 제품 모델"""

    id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=20)
    quantity = models.CharField(max_length=10)
    brand_name = models.CharField(max_length=20)
    original_price = models.IntegerField()
    sale_price = models.IntegerField()
    image_url = models.CharField(max_length=500)
    rank = models.IntegerField()
    total_rank = models.IntegerField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.display_name} - {self.brand_name} - {self.category}"
