from django.shortcuts import render
from django.http import HttpResponse
from common.models import NutriScopeData


# Create your views here.
def index(request):
    nutri_scope_data = NutriScopeData.objects.filter(category="프로틴")

    return render(
        request,
        "category/index.html",
        {"title": "Category Summary", "nutri_scope_data": nutri_scope_data},
    )
