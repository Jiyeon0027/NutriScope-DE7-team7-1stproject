from .models import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Brand():
    def __init__(self, brand_name:str):
        self.brand_name = brand_name
    
    def __str__(self):
        return f'브랜드 이름: {self.brand_name}' if self.brand_name else None
    
    
    def draw_top5_bar_chart(self, item: str = None):
        '''
        item을 인자로 받아 DB로부터 정보를 가져오고 인기 field top5를 수평으로 그려내는 함수\n
        args:\n
           item:\n 
           1. item이 없을경우: 클래스 인스턴스 생성시 만들어진 self.name을 담아 이용한다\n
           2. item이 있을경우: 메소드에 사용된 item을 담아 이용한다\n
        return: 인기 top 5개 브랜드의 bar차트가 수평으로 그려진 그래프를 json으로 변환하여 반환
        '''
        if not item:
            grouped_field = self.brand_name
        else:
            grouped_field = item

        results = list(FamousData.get_grouped_field_data(grouped_field))
        results.sort(key = lambda x: x['count'])
        x_value = []
        y_value = []
        
        for result in results:
            x_value.append(result.get("count"))
            y_value.append(result.get(grouped_field))

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


    def draw_brand_detail(self):
        '''
        brand_name을 입력값으로 받아 해당 브랜드의 카테고리(제품)를 파이차트로 그려내는 메소드\n
        args:\n
           self.name: 클래스 인스턴스 생성시 brand_name을 담아 객체 생성. draw_brand_detail() 메소드는 인스턴스의 self.name을 이용한다\n
        return: 해당 브랜드의 카테고리화된 아이템으로 구성된 파이차트의 json형식
        '''
        # args는 brand_name 필요하고, 데이터는 brand_name의 카테고리, count가 필요
        results = FamousData.get_brand_data_detail(self.brand_name, "category")
        values = []
        names = []

        for result in list(results):
            values.append(result.get("count"))
            names.append(result.get("category"))

        fig = px.pie(values=values, names=names)
        fig.update_traces(textinfo='label+percent')
        graph_json = fig.to_json()

        return graph_json