import re
import numpy as np
import pandas as pd
from django.db import transaction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import NutriScopeData


def remove_brand_from_product(product_name, brand_name):
    if not brand_name:
        return product_name or ""

    product = product_name or ""
    brand = str(brand_name)

    # 단어 경계를 고려해 브랜드 제거
    product = re.sub(r"\b" + re.escape(brand) + r"\b", "", product)
    # 연속된 공백 제거
    product = re.sub(r"\s+", " ", product).strip()
    return product


def group_similar_products(cosine_sim, threshold):
    n_products = cosine_sim.shape[0]
    visited = set()
    groups = []

    for i in range(n_products):
        if i in visited:
            continue
        similar_indices = np.where(cosine_sim[i] >= threshold)[0]
        if len(similar_indices) > 0:
            group = list(similar_indices)
            groups.append(group)
            visited.update(group)

    return groups


def select_representative_name(group_indices, df):
    group_names = df.iloc[group_indices]["product_name"].tolist()

    min_length = min(len(name) for name in group_names)
    shortest_names = [name for name in group_names if len(name) == min_length]

    representative = sorted(shortest_names)[0]
    return representative


def get_representative_name(threshold=0.6):
    """
    DB에 저장된 NutriScopeData의 product_name을 기반으로 대표 이름 생성 후 업데이트
    """
    # 1. DB -> DataFrame 로드
    qs = NutriScopeData.objects.all().values(
        "id", "product_name", "brand_name"
    )
    df = pd.DataFrame(list(qs))
    if df.empty:
        return

    # # 2. 브랜드명 제거한 tmp_product_name 생성
    df["tmp_product_name"] = df.apply(
        lambda row: remove_brand_from_product(row["product_name"], row["brand_name"]),
        axis=1,
    )

    # 3. TF-IDF + 코사인 유사도
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["tmp_product_name"].fillna(""))
    cosine_sim = cosine_similarity(tfidf_matrix)

    # 4. 그룹핑 & 대표 이름 할당
    groups = group_similar_products(cosine_sim, threshold)
    rep_map = {}
    for group in groups:
        rep_name = select_representative_name(group, df)
        for idx in group:
            rep_map[df.iloc[idx]["id"]] = rep_name

    # 6. DB 업데이트 (트랜잭션 처리)
    with transaction.atomic():
        for obj_id, rep_name in rep_map.items():
            NutriScopeData.objects.filter(id=obj_id).update(
                representative_name=rep_name
            )

def calc_total_rank():
    """
    representative_name별 rank 및 제품수 기준 score 계산 
    & total_rank 업데이트
    """
    # 1. DB -> DataFrame 로드
    qs = NutriScopeData.objects.all().values(
        'id', 'representative_name', 'rank'
    )
    df = pd.DataFrame(list(qs))
    if df.empty:
        return
    
    # 2. 그룹 통계 계산
    rep_name_stats = df.groupby('representative_name').agg({
        'rank': 'mean',
        'id': 'count'
    }).round(2)

    rep_name_stats.columns = ['avg_rank', 'product_count']
    rep_name_stats = rep_name_stats.reset_index() 
    
    # 3. combined_score 계산
    rep_name_stats['combined_score'] = (
        rep_name_stats['avg_rank'] / np.log1p(rep_name_stats['product_count'])
    )

    med_combined_score = np.median(rep_name_stats['combined_score'])
    rep_name_stats.loc[
        rep_name_stats['product_count'] <= 3, 'combined_score'
    ] += med_combined_score

    rep_name_stats['total_rank'] = (
        rep_name_stats['combined_score']
        .rank(method='dense', ascending=True)
        .astype(int)
    )
    
    # 4. representative_name -> total_rank 매핑
    rank_map = dict(
        zip(rep_name_stats['representative_name'], rep_name_stats['total_rank'])
    )
    
    # 5. ORM 객체 가져오기 & bulk_update
    ## 같은 representative_name에 rank값 한꺼번에 업데이트 하기
    objs = NutriScopeData.objects.all()
    for obj in objs:
        if obj.representative_name in rank_map:
            obj.total_rank = rank_map[obj.representative_name]

    with transaction.atomic():
        NutriScopeData.objects.bulk_update(objs, ['total_rank'])