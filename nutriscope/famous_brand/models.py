from django.db import models
from common.models import *
from django.db.models import Count
# Create your models here.

class FamousData(NutriScopeData):
    class Meta:
        proxy = True
    
    def get_grouped_field_data(groupfield: str):
        '''
        ## args를 group by로 조회하고, args가 나온 횟수를 count하여 보여줌\n
        args: \n
            groupfield: NutriScopeData의 field중 group by를 이용할 field\n
        return: args, count 로 이루어진 상위 5개의 값을 count가 높은순으로 정렬한(desc) 리스트
        '''
        
        data_list = NutriScopeData.objects.all()\
                    .values(groupfield)\
                    .annotate(count=Count(groupfield))\
        
        data_list = data_list.order_by("-count")[:5]

        return  data_list