"""공통 모델"""

from django.db import models


# Create your models here.
class NutriScopeData(models.Model):
    """공통 제품 모델"""

    id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=300)
    product_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    brand_name = models.CharField(max_length=50, null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    sale_price = models.IntegerField()
    image_url = models.CharField(max_length=500, null=True, blank=True)
    rank = models.IntegerField()
    category = models.CharField(max_length=30)
    representative_name = models.CharField(max_length=100, null=True, blank=True)
    total_rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.display_name} - {self.brand_name} - {self.category}"
