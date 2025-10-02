from django.shortcuts import render, HttpResponse
from django.views import View
from .controllers import *
# Create your views here.


class FamousBrandView(View):
    '''
    index 페이지용 클래스 뷰
    '''
    def get(self, request):
        brand_name = request.GET.get("brand_name", "brand_name") # query가 있을경우 "brand_name"을 인자로 받는다. 없을경우 "brand_name"을 default로 리턴
        graph_json = Brand(brand_name).draw_top5_bar_chart()

        return render(request, 'index.html', {'graph_json': graph_json})
    
    
class FamousBrandDetailView(View):
    '''
    디테일 페이지용 클래스 뷰
    '''
    def get(self, request):
        brand_name = request.GET.get("brand_name")
        graph_json = Brand(brand_name).draw_brand_detail()

        return HttpResponse(graph_json)