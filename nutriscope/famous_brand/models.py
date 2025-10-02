from django.db import models
from common.models import *
from django.db.models import Count
# Create your models here.

class FamousData(NutriScopeData):
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