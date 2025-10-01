from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import NutriScopeData
from .utils import get_representative_name, calc_total_rank

@receiver([post_save, post_delete], sender=NutriScopeData)
def update_representative_names(sender, **kwargs):
    """
    NutriScopeData가 추가/수정/삭제될 때
    1. representative_name 갱신
    2. total_rank 갱신
    순서대로 실행
    """
    get_representative_name()
    calc_total_rank()