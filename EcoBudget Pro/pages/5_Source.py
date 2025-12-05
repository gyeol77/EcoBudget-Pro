import streamlit as st

st.set_page_config(
    page_title="EcoBudget Pro - Source",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Source")
st.caption("탄소 배출량 계산 기준 및 데이터 출처, EcoScore 계산 방식")

st.markdown("---")

st.subheader("탄소 배출량 계산 기준 및 데이터 출처")
st.markdown(
    """
    EcoBudget Pro에서 사용하는 카테고리별 탄소계수(`CARBON_FACTOR`)는  
    국제 기관의 공식 환경 데이터(LCA 기반)를 참고하여,  
    카테고리별 평균 배출 강도를 “kg CO₂e / 10,000원 소비 기준”으로  
    정규화한 추정치입니다.

    ### 참고 자료(References)

    - IPCC AR6 (2021): Industrial & Transportation Emission Factors  
    - UNEP (2020): Fashion Industry Carbon Footprint  
    - FAO (2021): Foodprint Database  
    - IEA (2022): Energy Emission Factors by Sector  
    - EPA (2019): Household Chemical & Plastic Product Emissions  
    - NHS (2019): Healthcare Carbon Footprint  
    - University of Manchester (2020): Cultural Activity LCA Study  
    - OECD (2019): Educational Emission Intensity  

    ※ 모든 수치는 비교를 위한 범용적 평균값이며,  
    실제 개별 소비·상품의 배출량과는 다소 차이가 있을 수 있습니다.
    """
)

st.markdown("---")

st.subheader("EcoScore (친환경 점수) 계산 방식")
st.markdown(
    """
    EcoBudget Pro는 한 달 기준 총 탄소 배출량(kg CO₂e)을  
    0~100점 사이의 **EcoScore**로 변환하여,  
    현재 소비 패턴의 친환경 정도를 직관적으로 표현합니다.

    점수는 총 배출량 구간에 따라 다음과 같이 계산됩니다.

    ```python
    def eco_score(total_carbon: float) -> float:
        if total_carbon <= 20:
            return 100.0
        elif total_carbon <= 50:
            return 100 - (total_carbon - 20) * 1.3
        else:
            return max(0.0, 60 - (total_carbon - 50) * 0.8)
    ```

    - **20kg 이하**: 매우 낮은 배출 구간으로 간주하며, 항상 **100점**을 부여합니다.  
    - **20~50kg**: 배출량이 늘어날수록 점수가 완만하게 감소하며,  
      대략 **1kg 증가당 약 1.3점**씩 감소합니다.  
      (예: 20kg → 100점, 35kg → 약 80점, 50kg → 약 61점 수준)  
    - **50kg 초과**: 과다 배출 구간으로 간주하여 점수를 더 가파르게 감소시키며,  
      **1kg 증가당 약 0.8점**씩 감소하고, 최소 점수는 **0점**입니다.

    사용자에게 다소 낯설고 추상적일 수 있는 '몇 kg CO₂e인지'만 제공하는 것이 아니라,  
    상대적인 친환경 점수(0~100점)를 통해 자신의 소비 패턴을 쉽게 파악하고 
    친환경 정도가 현실적으로 와닿을 수 있도록 설계되었습니다.
    """
)