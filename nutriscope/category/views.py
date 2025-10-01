from django.shortcuts import render
from django.http import HttpResponse
from common.models import NutriScopeData


# Create your views here.
def index(request):
    protain = NutriScopeData.objects.filter(category="프로틴")
    probiotic = NutriScopeData.objects.filter(category="유산균/프로바이오틱")
    vitamin = NutriScopeData.objects.filter(category="비타민")
    ginseng = NutriScopeData.objects.filter(category="홍삼/인삼")
    magnesium = NutriScopeData.objects.filter(category="마그네슘")
    etc = NutriScopeData.objects.filter(category="기타")
    omega3 = NutriScopeData.objects.filter(category="오메가3")
    enzyme = NutriScopeData.objects.filter(category="효소")
    juice = NutriScopeData.objects.filter(category="녹즙/주스")
    honey = NutriScopeData.objects.filter(category="꿀")
    collagen = NutriScopeData.objects.filter(category="콜라겐")
    etc_health = NutriScopeData.objects.filter(category="기타 건강식품")
    lutein = NutriScopeData.objects.filter(category="루테인")
    biotin = NutriScopeData.objects.filter(category="비오틴")
    zinc = NutriScopeData.objects.filter(category="아연")
    calcium = NutriScopeData.objects.filter(category="칼슘")
    milk_cysteine = NutriScopeData.objects.filter(category="밀크씨슬")

    data = {
        "단백질": protain,
        "유산균/프로바이오틱": probiotic,
        "비타민": vitamin,
        "홍삼/인삼": ginseng,
        "마그네슘": magnesium,
        "기타": etc,
        "오메가3": omega3,
        "효소": enzyme,
        "녹즙/주스": juice,
        "꿀": honey,
        "콜라겐": collagen,
        "기타 건강식품": etc_health,
        "루테인": lutein,
        "비오틴": biotin,
        "아연": zinc,
        "칼슘": calcium,
        "밀크씨슬": milk_cysteine,
    }

    # items()를 사용하여 키-값 쌍을 전달
    data_items = data.items()

    return render(
        request,
        "category/index.html",
        {
            "title": "Category Summary",
            "data_items": data_items,
        },
    )
