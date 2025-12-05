# 🌿 EcoBudget Pro
> 영수증 기반 개인 탄소 발자국 · 소비 패턴 분석 도구

EcoBudget Pro는 일상의 소비 데이터(영수증)를 기반으로  
카테고리 자동 분류 → 탄소 배출량 분석 → EcoScore 산출 → 개선 방향 추천  
까지 한 번에 제공하는 분석 애플리케이션입니다.

Streamlit 기반 인터페이스를 활용해 CSV 데이터를 업로드하면 바로 분석 결과를 확인할 수 있으며,  
시각화 및 점수화, 개선 방향 가이드까지 이어지는 흐름으로 사용자 친화적인 경험을 제공합니다.

---

## ✨ 주요 기능 (Features)

### 📥 CSV 업로드 & 전처리
- 품목명 기반 자동 카테고리 분류  
- 카테고리별 탄소 배출량 계산  

### 📊 시각화 (Visualization)
- 카테고리별 배출량 요약 테이블  
- Bar / Pie 차트 시각화  
- 상위 카테고리 강조 표시  

### 🌱 EcoScore (0~100)
- 전체 탄소 배출량을 친환경 점수로 정규화  
- 점수 구간에 따른 등급(A~D) 부여  
- 카테고리별 배출 기여도 분석  

### 💡 개선 추천 (Recommendation)
- 배출량 상위 3개 카테고리 중심 소비 절감 시나리오  
- 감축 비율(예: 10%, 20%, 30%)에 따른 탄소 감축량 계산  
- 자동차 주행 거리, 전기 사용량, 나무 심기 효과로 환산(체감 효과 증대) 
- EcoScore 개선 시나리오

### 📚 Source
- 카테고리별 탄소계수(CARBON_FACTOR) 출처 정리  
- EcoScore 계산 방식 및 점수 기준 설명  

---

## 📸 예시 화면 (Screenshots)

### 1) Visualization 화면

<p align="center">
  <img src="EcoBudget%20Pro/images/Visualization.png" width="700">
</p>

<p align="center">
  <img src="EcoBudget%20Pro/images/EcoScore.png" width="700">
</p>

---

## 🧱 프로젝트 구조 (Project Structure)

    EcoBudget-Pro/
    ├─ app.py                    # 메인 소개 페이지
    ├─ pages/
    │  ├─ 1_Upload_Data.py       # CSV 업로드 및 전처리
    │  ├─ 2_Visualization.py     # 시각화
    │  ├─ 3_EcoScore.py          # EcoScore 분석
    │  ├─ 4_Recommendation.py    # 개선 시나리오 및 추천
    │  └─ 5_Source.py            # 탄소계수 & EcoScore 계산 기준
    └─ utils/
       ├─ carbon.py              # 탄소계수 / 탄소량 계산
       ├─ categorize.py          # 품목명 → 카테고리 분류
       └─ scoring.py             # EcoScore 계산 함수
    ...
---

## 📄 입력 데이터 형식 (CSV Format)

필수 항목은 다음과 같습니다.

- date  : 날짜 (예: 2025-11-01)  
- item  : 품목명 (예: 아메리카노, 택시)  
- price : 가격(원 단위, 정수/실수)  

예시:

    date,item,price
    2025-11-01,아메리카노,4500
    2025-11-01,택시,30000
    2025-11-02,이어폰,25000

업로드 후 애플리케이션에서 자동으로 다음 두 항목이 추가됩니다.

- category  : 품목명 기반 카테고리 자동 분류  
- carbon_kg : 탄소 배출량(kg CO₂e)  

---

## 🚀 실행 방법 (How to Run)

### 1) requirements 설치

프로젝트 실행에 필요한 패키지는 'requirements.txt' 파일에 포함되어 있습니다.  
해당 파일은 아래 경로에 위치합니다:

    EcoBudget Pro/requirements.txt

아래 명령어로  설치할 수 있습니다:

    pip install -r "EcoBudget Pro/requirements.txt"

### 2) Streamlit 앱 실행

아래 명령어로 애플리케이션을 실행합니다:

    streamlit run "EcoBudget Pro/app.py"

기본 접속 주소:

    http://localhost:8501

---

### 📂 샘플 데이터 (Sample Data)

테스트용 CSV 파일이 `assets/` 폴더에 포함되어 있습니다.

- **파일명:** `sample.csv`  
- **위치:** `assets/sample.csv`

이 파일을 **Upload 페이지에서 업로드하면**,  
전체 분석 기능을 바로 체험할 수 있습니다.
(카테고리 자동 분류 → 탄소 배출량 계산 → 시각화 → EcoScore → 추천)

---

## 🌍 탄소 배출 계수 (Carbon Emission Factors)

탄소 배출량은 `utils/carbon.py`에 정의된 `CARBON_FACTOR`를 이용해 계산합니다.

    CARBON_FACTOR = {
        "교통": 2.8,
        "식음료": 1.5,
        "패션/미용": 4.0,
        "생활용품": 3.2,
        "전자기기": 5.0,
        "문화/여가": 1.2,
        "의료/건강": 2.0,
        "교육/자기계발": 1.0,
        "주거/공과금": 3.5,
        "기타": 1.0,
    }

각 항목의 탄소 배출량은 다음과 같이 계산합니다.

    carbon_kg = (price / 10000) * CARBON_FACTOR[category]

### 참고한 주요 출처 (대표 LCA 기반 데이터)

- IPCC AR6 (2021)  
- UNEP (2020)  
- FAO (2021)  
- IEA (2022)  
- EPA (2019)  
- NHS (2019)  
- University of Manchester LCA Study (2020)  
- OECD (2019)  

> 위 탄소계수는 카테고리별 평균값을 단순화한 추정치이며,  
> 실제 개별 상품·서비스의 탄소 배출량과는 차이가 있을 수 있습니다.

---

## 🌱 EcoScore 계산 방식

EcoScore는 일정 기간의 **총 탄소 배출량(kg CO₂e)** 을  
0~100점 사이의 점수로 변환한 지표입니다.  
계산 로직은 `utils/scoring.py`에 정의되어 있습니다.

    def eco_score(total_carbon):
        if total_carbon <= 20:
            return 100.0
        elif total_carbon <= 50:
            return round(100 - (total_carbon - 20) * 1.3, 1)
        else:
            return max(0.0, round(60 - (total_carbon - 50) * 0.8, 1))

### 점수 구간 요약

- 0~20kg  : 매우 낮은 배출량 → 100점  
- 20~50kg : 1kg 증가당 약 1.3점 감소  
- 50kg↑   : 1kg 증가당 약 0.8점 감소 (최소 0점)  

EcoScore는 사용자의 소비 패턴을 **직관적으로 비교·평가하기 위한 상대적 지표**로 설계되었습니다.

---

## ⚠️ 한계 및 유의 사항

- 탄소 배출량은 **카테고리별 평균값 기반 추정치**입니다.  
- EcoScore와 개선 시나리오 결과는 **단순화된 모델에 의한 계산 결과**이며, 실제 탄소배출과 다소 차이가 있을 수 있습니다.   
- 절대적 수치보다는 **카테고리 간 상대적 크기와 소비 경향**을 파악하는 용도로 사용하는 것이 적절합니다.

---

## 🎯 프로젝트 목적 (Summary)

EcoBudget Pro는 일상의 소비 내역을 환경적 관점에서 재해석하여,

- 어떤 카테고리에서 탄소를 많이 배출하고 있는지  
- EcoScore를 높이기 위해 어떤 소비를 먼저 줄여야 하는지  
- 현재 나의 소비 패턴이 얼마나 친환경적인지  

를 직관적으로 이해할 수 있도록 돕는 것을 목표로 합니다.

개인이 손쉽게 자신의 탄소 발자국을 점검하고,  
작은 행동 변화를 통해 더 친환경적인 소비를 실천하도록 지원하는 도구입니다.
감사합니다.

---
