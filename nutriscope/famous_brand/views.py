from django.shortcuts import render, HttpResponse
from django.views import View
from .chartbuilder import *
# Create your views here.


class FamousBrandView(View):
    '''
    index 페이지용 클래스 뷰
    '''
    def get(self, request):
        brand_name = request.GET.get("brand_name", "brand_name") # query가 있을경우 "brand_name"을 인자로 받는다. 없을경우 "brand_name"을 default로 리턴
        graph_json_bar = Brand().draw_top_chart('bar')
        graph_json_pie = Brand().draw_top_chart('pie')

        return render(request, 'index.html', {'graph_json_bar': graph_json_bar, 'graph_json_pie': graph_json_pie})
    
    
class FamousBrandDetailView(View):
    '''
    디테일 페이지용 클래스 뷰
    '''
    def get(self, request):
        brand_name = request.GET.get("brand_name")
        graph_json = Brand(brand_name).draw_brand_detail("pie")

        return HttpResponse(graph_json)