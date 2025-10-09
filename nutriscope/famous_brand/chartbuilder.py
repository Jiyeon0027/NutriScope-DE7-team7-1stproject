from .models import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

    
class ChartBuilder():
    def __init__(self):
        self.color_list = ["#B8E6E9", '#FFC19E', '#FFE08C', '#6699FF', '#F15F5F', '#FFB2D9', '#3DB7CC', '#CC3D3D', "#E386FF", "#4ED898"]
        self.brand_name = "brand_name"

    def draw_top_chart(self, chart_type: str, nums: int = 10, grouping_field: str = "brand_name"):
        '''
        DB로부터 정보를 가져오고 그룹화 된 field를 nums 갯수만큼 bar 또는 pie 형식으로 그려내는 함수\n
        args:\n
        -> chart_type: 'bar' 혹은 'pie'\n
        -> nums: 그래프 내부 item의 개수\n
        -> grouping_field: 그룹화를 원하는 filed\n 
        return: 인기 top nums개 브랜드의 수평으로 그려진 bar or pie 차트를 json으로 변환하여 반환
        '''
        if nums > 10:
            raise ValueError("순위는 10등까지만 조회 가능합니다")

        results = list(FamousData.get_grouped_field_data(grouping_field, nums))

        if chart_type == 'bar':
            x_value = []
            y_value = []
            
            for result in results:
                x_value.append(result.get("count"))
                y_value.append(result.get(grouping_field))

            fig = go.Figure(
                data=[go.Bar(x=x_value, y=y_value, orientation='h', marker_color=self.color_list[:nums])], # orientation=h 옵션을 줌으로 수평 그래프를 만들어냄
                layout=go.Layout(
                    title=go.layout.Title(text=f"Top{nums} 인기 브랜드"),
                    yaxis={'categoryorder': 'total ascending'},  # 제일 높은값이 제일 위로 가게 만드는 layout
                    width=632,
                    height=479,
                    autosize=True,
                    clickmode='event'
                )
            )

            return fig
        
        elif chart_type == "pie":
            values = []
            names = []

            for result in list(results):
                values.append(result.get("count"))
                names.append(result.get(grouping_field))
            
            fig = go.Figure(data=[
            go.Pie(
                labels=names,
                values=values,
                hole = 0.4
            )
            ])
            fig.update_layout(
                title=f"Top {nums} 브랜드 비율",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Pretendard, sans-serif"),
                margin=dict(t=60, b=40, l=40, r=40)
            )

            return fig
        
        else:
            raise ValueError("chart_type은 'pie' 혹은 'bar'형태로만 가능합니다")
        
    def draw_brand_detail(self, chart_type: str):
        '''
        brand_name을 입력값으로 받아 해당 브랜드의 카테고리(제품)를 파이차트로 그려내는 메소드\n
        args:\n
        -> self.name: 클래스 인스턴스 생성시 brand_name을 담아 객체 생성. draw_brand_detail() 메소드는 인스턴스의 self.name을 이용한다\n
        return: 해당 브랜드의 카테고리화된 아이템으로 구성된 bar or pie차트의 json형식
        '''
        if chart_type == 'bar':
            results = FamousData.get_brand_data_detail(self.brand_name, "category")
            x_value = []
            y_value = []
            
            for result in results:
                x_value.append(result.get("count"))
                y_value.append(result.get("category"))

            fig = go.Figure(
                data=[go.Bar(x=x_value, y=y_value, orientation='h', marker_color=self.color_list[:len(results)])], # orientation=h 옵션을 줌으로 수평 그래프를 만들어냄
                layout=go.Layout(
                    title=go.layout.Title(text=f"{self.brand_name} 제품 비중"),
                    yaxis={'categoryorder': 'total ascending'},  # 제일 높은값이 제일 위로 가게 만드는 layout
                    width=632,
                    height=479,
                    autosize=True,
                    clickmode='event'
                )
            )

            fig = fig.to_json()
            return fig
        
        elif chart_type == 'pie':
            results = FamousData.get_brand_data_detail(self.brand_name, "category")
            values = []
            names = []

            for result in list(results):
                values.append(result.get("count"))
                names.append(result.get("category"))

            fig = go.Figure(data=[
                go.Pie(
                    labels = names,
                    values = values,
                    hole = 0.4
                )
                ])
            fig.update_layout(
                title=f"{self.brand_name} 제품 비중",
                height = 632,
                width = 632
            )

            fig = fig.to_json()
            return fig
        
        else: 
            raise ValueError("chart_type은 'pie' 혹은 'bar'형태로만 가능합니다")

    

class Brand(ChartBuilder):
    def __init__(self, brand_name:str = None):
        super().__init__()
        if brand_name:
            self.brand_name = brand_name
        
    def __str__(self):
        return f'브랜드 이름: {self.brand_name}' if self.brand_name else None
