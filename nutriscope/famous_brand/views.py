from django.shortcuts import render
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
        results = list(FamousData.get_grouped_field_data("brand_name"))
        x_value = []
        y_value = []
        
        for result in results:
            x_value.append(result.get("brand_name"))
            y_value.append(result.get("count"))

        fig = go.Figure(
            data=[go.Bar(x=x_value, y=y_value)],
            layout=go.Layout(
                title=go.layout.Title(text="Top5 인기 브랜드")
            )
        )

        fig.write_html("../sample.html")

        return 