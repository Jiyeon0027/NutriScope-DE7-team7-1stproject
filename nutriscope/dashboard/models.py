from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)  # 자동 증가 ID
    shop_name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=20)
    quantity = models.CharField(max_length=10)
    brand_name = models.CharField(max_length=20)
    original_price = models.IntegerField(null=True, blank=True)
    sale_price = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=500)
    rank = models.IntegerField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product_name} ({self.brand_name})"
