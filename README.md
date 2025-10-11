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

## 🎯 주요 기능

### 📊 대시보드 (Dashboard)

- **메인 대시보드**: 전체 데이터 개요 및 통계
- **제품 비교**: 동일 제품의 쇼핑몰별 가격 비교
- **카테고리-가격 분석**: 카테고리별 가격 분포 시각화
- **제품 목록**: 검색 및 정렬 기능이 있는 제품 리스트

### 🏷️ 카테고리 분석 (Category)

- **17개 세분화된 카테고리**: 비타민, 홍삼/인삼, 유산균/프로바이오틱 등
- **카테고리별 상세 분석**: 제품 수, 가격 분포, 브랜드 분석
- **인터랙티브 차트**: Plotly를 활용한 동적 시각화

### 🏆 순위 분석 (Ranking)

- **종합 순위**: 쇼핑몰별, 카테고리별 제품 순위
- **가격 대비 성능 분석**: 가성비 기반 순위 제공

### 🌟 유명 브랜드 분석 (Famous Brand)

- **브랜드별 제품 분석**: 인기 브랜드 Top-N 분석
- **브랜드 시장 점유율**: 파이차트 및 바차트로 시각화

### 🏪 쇼핑몰별 특성

- **iHerb**: 해외 건강기능식품 전문, 다양한 비타민과 미네랄
- **G마켓**: 한국 전통 건강식품과 일상 건강식품 중심
- **카카오 선물하기**: 선물용 건강식품 중심, 고급 브랜드
- **마켓컬리**: 일상 건강관리 제품, 신선식품과 함께 판매

## 🛠️ 기술 스택

### Backend

- **Django 5.2.6**: 웹 프레임워크
- **Django REST Framework**: API 개발
- **SQLite**: 데이터베이스

### Frontend

- **HTML/CSS/JavaScript**: 기본 웹 기술
- **Plotly**: 인터랙티브 차트 및 시각화
- **Bootstrap**: 반응형 UI 프레임워크

### Data Processing

- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산
- **Scikit-learn**: 데이터 전처리 및 그룹핑

### Development Tools

- **Python 3.11**: 프로그래밍 언어

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

- 전체 데이터 통계 및 개요
- 쇼핑몰별 제품 분포 파이차트
- 최근 제품 목록

### 2. 제품 비교

- 동일 제품의 쇼핑몰별 가격 비교
- 가격 차이 시각화
- 최적 구매처 추천

### 3. 카테고리 분석

- 17개 카테고리별 상세 분석
- 인터랙티브 트리맵 및 바차트
- 카테고리별 가격 분포

### 4. 순위 분석

- 종합 순위 및 가성비 분석
- 쇼핑몰별 순위 비교
