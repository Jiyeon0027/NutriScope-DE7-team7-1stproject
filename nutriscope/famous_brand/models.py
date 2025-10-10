from django.db import models
from common.models import *
from django.db.models import Count
# Create your models here.

class BrandData(NutriScopeData):
    class Meta:
        proxy = True
    
    def get_grouped_field_data(groupfield: str, nums: int):
        '''
        ## args를 group by로 조회하고, args가 나온 횟수를 count하여 보여줌\n
        args: \n
            groupfield: NutriScopeData의 field중 group by를 이용할 field\n
        return: args, count 로 이루어진 상위 5개의 값을 count가 높은순으로 정렬한(desc) 리스트
        '''
        
        data_list = NutriScopeData.objects.all()\
                    .values(groupfield)\
                    .annotate(count=Count(groupfield))\
        
        data_list = data_list.order_by("-count")[:nums]

        return  data_list
    
    def get_brand_data_detail(brand_name: str, groupfield: str):
        '''
        ## args를 조건으로 1차 조회, 데이터를 다시 groupfield별로 group화 하여 count를 세어 반환\n
        args: \n
            brand_name: 검색하고자 하는 브랜드 이름\n
            groupfield: NutriScopeData의 field중 group by를 이용할 field\n
        return: brand_name, groupfield, count를 count가 높은순으로 정렬한 리스트
        '''

        brand_data_list = NutriScopeData.objects.filter(brand_name=brand_name)
        grouped_brand_data_list = brand_data_list.values(groupfield).annotate(count=Count(groupfield))

        return grouped_brand_data_list
    
    def get_brand_data_table(brand_name: str):
        '''
        ## brand_name을 받아 해당 브랜드에 속해있는 모든 정보를 가져와 테이블에 사용할 필드의 데이터를 반환\n
        args:\n
            brnad_name: 검색하고자 하는 브랜드 이름
        return: NutriScopeData 테이블의 해당 브랜드 명으로 등록된 필드의 테이블 용 데이터
        '''

        brand_data_list = NutriScopeData.objects.filter(brand_name=brand_name)
        filterd_brand_data_list = brand_data_list.values("image_url", "brand_name", "product_name", "shop_name", "rank")
        # brand_data_list = NutriScopeData.objects.values("image_url", "brand_name", "product_name", "rank")
        rank_ordered_data = filterd_brand_data_list.order_by("rank")

        return rank_ordered_data
    
