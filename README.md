# 🥗 NutriScope - 건강식품 가격 비교 플랫폼

**데이터 엔지니어링 데브코스 [Team7] 작은 불꽃 연구회 - 1차 프로젝트**

> 4개 주요 쇼핑몰의 건강식품 데이터를 수집하고 분석하여 최적의 구매 정보를 제공하는 웹 플랫폼

## 📋 프로젝트 개요

### 🎯 목표

- 4개 쇼핑몰(마켓컬리, iHerb, 카카오 선물하기, G마켓)의 건강식품 데이터 수집
- 동일 제품의 가격 비교 및 종합 순위 제공
- 건강식품 카테고리별 시각화 및 분석 결과 제공
- 인터랙티브 대시보드를 통한 데이터 탐색 및 분석

### 👥 팀 구성

- **김지연**: 카카오 선물하기 크롤링, 카테고리별 그래프, 발표
- **이성진**: iHerb 크롤링, 기타 카테고리 재분류 전처리, 인기 브랜드 Top-N 분석
- **최규영**: 마켓컬리 크롤링, 가격 분포 그래프, 레이아웃 생성
- **김소정**: G마켓 크롤링, 상품명, 갯수 등 데이터 전처리, 종합 순위 로직 설계

## 🏗️ 프로젝트 구조

```
├── data/                          # 데이터 관련 파일
│   ├── merged-id-data/           # ID가 포함된 병합 데이터
│   ├── non-id/                   # ID가 없는 데이터
│   ├── original_data/            # 원본 크롤링 데이터
│   └── preprocessed-data/        # 전처리된 데이터
├── nutriscope/                   # Django 프로젝트
│   ├── common/                   # 공통 앱 (메인 모델)
│   ├── dashboard/                # 대시보드 앱
│   ├── category/                 # 카테고리 분석 앱
│   ├── ranking/                  # 순위 분석 앱
│   ├── famous_brand/             # 유명 브랜드 분석 앱
│   └── nutriscope/               # Django 기본 설정 파일
├── requirements.txt              # Python 의존성
└── README.md                     # 프로젝트 문서
```

## 🛠️ 기술 스택

### Backend

- **Django**: 웹 프레임워크
- **SQLite**: 데이터베이스

### Frontend

- **HTML/CSS/JavaScript**: 기본 웹 기술
- **Plotly**: 인터랙티브 차트 및 시각화
- **Bootstrap**: 반응형 UI 프레임워크

### Data Processing

- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산
- **Scikit-learn**: 데이터 전처리 및 그룹핑

### 페이지 라우팅

- `/`: 메인 대시보드
- `/product-comparison/`: 제품 비교 페이지
- `/compare-table/`: 비교 테이블
- `/product-list/`: 제품 목록
- `/category-price/`: 카테고리-가격 분석
- `/category/`: 카테고리 분석
- `/ranking/`: 순위 분석
- `/famous_brand/`: 유명 브랜드 분석

## 📊 데이터 모델

### 🏪 데이터를 가져온 쇼핑물

- **iHerb**: 해외 건강기능식품 전문, 다양한 비타민과 미네랄
- **G마켓**: 한국 전통 건강식품과 일상 건강식품 중심
- **카카오 선물하기**: 선물용 건강식품 중심, 고급 브랜드
- **마켓컬리**: 일상 건강관리 제품, 신선식품과 함께 판매

### NutriScopeData 모델

```python
class NutriScopeData(models.Model):
    id = models.IntegerField(primary_key=True)
    shop_name = models.CharField(max_length=50)          # 쇼핑몰명
    display_name = models.CharField(max_length=300)      # 표시명
    product_name = models.CharField(max_length=100)      # 제품명
    quantity = models.CharField(max_length=50)           # 수량
    brand_name = models.CharField(max_length=50)         # 브랜드명
    original_price = models.FloatField()                 # 원가
    sale_price = models.IntegerField()                   # 판매가
    image_url = models.CharField(max_length=500)         # 이미지 URL
    rank = models.IntegerField()                         # 순위
    category = models.CharField(max_length=30)           # 카테고리
    representative_name = models.CharField(max_length=100) # 대표명
    total_rank = models.IntegerField()                   # 전체 순위
```

## 🎨 주요 화면

### 1. 메인 대시보드

- 총 제품 수, 평균 가격, 브랜드 수, 카테고리 수 수치를 나타냄
- 가격 분포, 인기 브랜드, 카테고리 별 제품 수를 그래프로 나타냄

<p align="center">
<img width="70%" alt="대시보드 이미지" src="https://github.com/user-attachments/assets/704532ee-7440-42ad-8ae5-6989642be9c1" />
</p>

### 2. 인기브랜드 팝업

- 상위 10개 제품 브랜드의 bar 차트 및 pie 차트 시각화
- 차트내 brand_name을 클릭 시 모달창을 이용해 다음의 기능을 보여준다
    - bar chart: 제품군 비중
    - pie chart: 제품군 테이블

<p align="center">
<img width="70%" alt="brand_img" src="https://github.com/user-attachments/assets/a6c2b450-428f-40aa-ad5b-3cce580226d9" />
</p>

### 3. 상품리스트 / 상품 목록 - 데이터 검색

- 상품명, 브랜드명, 쇼핑몰 정보를 입력하면 해당하는 데이터 목록을 출력
- 출력된 데이터를 id, 가격 기준으로 정렬
- 검색된 데이터 기반의 제품 수, 평균 가격, 쇼핑몰 별 제품 비율 정보 업데이트

<p align="center">
<img width="70%" alt="products" src="https://github.com/user-attachments/assets/53a2fe9a-dc3c-46c6-a6cd-1ceed3c0a399" />
</p>

### 4. 랭킹

- 페이지의 왼쪽에 최근 인기 있는 순위로 제품군
- 보고 싶은 제품군을 클릭하면 페이지의 오른쪽 부분에서 해당 군에 속하는 제품들의 가격과 구성을 비교

<p align="center">
<img width="70%" alt="ranking" src="https://github.com/user-attachments/assets/122ff26b-c4d3-4bfd-9668-49707f7b25c3" />
</p>

### 5. 카테고리 별 시각화

- **카테고리 분석 페이지**
    - 총 17개의 카테고리를 막대그래프와 파이 그래프로 생성
    - 각각의 카테고리를 클릭 시 그 내부의 상품들이 어떤 것인지 랭킹별로 보여줌

<p align="center">
<img width="70%" alt="category1" src="https://github.com/user-attachments/assets/db4c77b1-4b0d-425a-a6c6-0a7392a1df7c" />
</p>

- **카테고리별 보기**
    - 카테고리 별 제품 수를 나타내는 트리맵 그래프 클릭 시, 선택된 항목의 값을 기준으로 상품 목록과 막대 그래프가 함께 갱신
      
<p align="center">
<img width="70%" alt="category2" src="https://github.com/user-attachments/assets/668a3b91-7bd5-414d-b4f1-9a53af16b324" />
</p>
