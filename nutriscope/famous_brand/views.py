from django.shortcuts import render, HttpResponse
from django.views import View
from .models import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Create your views here.

class Brand():
    def __init__(self, brand_name:str = None):
        if brand_name:
            self.brand_name = brand_name
    
    def __str__(self):
        return f'브랜드 이름: {self.brand_name}' if self.brand_name else None
    
    
    def draw_top_famousbrand():
        '''
        DB로부터 정보를 가져와 인기 브랜드 top5를 그려내는 함수 수평으로 그려내는 함수
        '''
        results = list(FamousData.get_grouped_field_data("brand_name"))
        results.sort(key = lambda x: x['count'])
        x_value = []
        y_value = []
        
        for result in results:
            x_value.append(result.get("count"))
            y_value.append(result.get("brand_name"))

        color_list = ['#A366FF', '#FFC19E', '#FFE08C', '#6699FF', '#F15F5F']

        fig = go.Figure(
            data=[go.Bar(x=x_value, y=y_value, orientation='h', marker_color=color_list)], # orientation=h 옵션을 줌으로 수평 그래프를 만들어냄
            layout=go.Layout(
                title=go.layout.Title(text="Top5 인기 브랜드"),
                yaxis={'categoryorder': 'total ascending'},  # 제일 높은값이 제일 위로 가게 만드는 layout
                width=500,
                height=370,
                autosize=True,
                clickmode='event'
            )
        )
       
        graph_json = fig.to_json()
        
        return graph_json
        # graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        # return graph_html

    def draw_brand_detail(self):
        '''
        brand_name을 입력값으로 받아 해당 브랜드의 카테고리(제품)를 파이차트로 그려내는 함수
        '''
        # args는 brand_name 필요하고, 데이터는 brand_name의 카테고리, count가 필요
        results = FamousData.get_brand_data_detail(self.brand_name, "category")
        values = []
        names = []
        results_length = len(results)
        # pull_list = 

        for result in list(results):
            values.append(result.get("count"))
            names.append(result.get("category"))

        fig = px.pie(values=values, names=names)
        graph_json = fig.to_json()
        # fig.update_traces(pull=[0])
        # fig.write_html("../sample.html")

        return graph_json


class FamousBrandView(View):
    def get(self, request):
        graph_json = Brand.draw_top_famousbrand()

        return render(request, 'index.html', {'graph_json': graph_json})
    
class FamousBrandDetailView(View):
    def get(self, request):
        brand_name = request.GET.get("brand_name")
        graph_json = Brand(brand_name).draw_brand_detail()

        return HttpResponse(graph_json)