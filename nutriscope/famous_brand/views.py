from django.shortcuts import render
from django.views import View
from .models import *
import plotly.express as px
import plotly.graph_objects as go
# Create your views here.

class Brand():
    def __init__(self, brand_name:str = None):
        if brand_name:
            self.brand_name = brand_name
    
    def __str__(self):
        return print(f'브랜드 이름: {self.brand_name}') if self.brand_name else None
    
    
    def draw_top_famousbrand():
        '''
        DB로부터 정보를 가져와 인기 브랜드 top5를 그려내는 함수 수평으로 그려내는 함수
        '''
        results = list(FamousData.get_grouped_field_data("brand_name"))
        x_value = []
        y_value = []
        
        for result in results:
            x_value.append(result.get("count"))
            y_value.append(result.get("brand_name"))

        fig = go.Figure(
            data=[go.Bar(x=x_value, y=y_value, orientation='h')], # orientation=h 옵션을 줌으로 수평 그래프를 만들어냄
            layout=go.Layout(
                title=go.layout.Title(text="Top5 인기 브랜드"),
                yaxis={'categoryorder': 'total ascending'},  # 제일 높은값이 제일 위로 가게 만드는 layout
                autosize=True
            )
        )

        graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        return graph_html
    


class FamousBrandView(View):
    def get(self, request):
        graph_html = Brand.draw_top_famousbrand()

        return render(request, 'index.html', {"graph_html": graph_html})
    