import streamlit as st

st.set_page_config(
    page_title="EcoBudget Pro",
    page_icon="🌿",
    layout="wide",
)

st.title("🌿 EcoBudget Pro")
st.caption("영수증 기반 탄소 발자국 · 소비 패턴 분석 및 개선")

st.markdown("---")

st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("프로젝트 소개")
st.markdown(
    """
    **EcoBudget Pro**는 영수증(소비 내역) 데이터를 기반으로,

    - 💸 카테고리별 소비 패턴 분석  
    - 🌍 탄소 배출량(탄소 발자국) 추정  
    - ✅ 친환경적 소비를 위한 개선 방향 제안

    위와 같은 일련의 과정이 이루어지는 프로젝트입니다. 

    사용자는 데이터를 업로드한 뒤, 각 페이지(좌측 페이지 바)를 통해  
    **시각화 → EcoScore 확인 → 개선 방향**의 흐름으로  
    자신의 소비와 탄소 배출 특성을 한눈에 파악하고 개선할 수 있습니다.
    """
)

st.markdown("---")

st.subheader("사용 가이드")
st.markdown(
    """
    1️⃣ **Upload Data**  
    └ 영수증과 같은 소비 내역이 정리된 **CSV** 파일을 업로드합니다.  

    2️⃣ **Visualization**  
    └ 기간·카테고리별 소비 금액과 탄소 배출량을 그래프로 확인합니다.  

    3️⃣ **EcoScore**  
    └ 일정 기간과 카테고리를 기준으로 EcoScore를 계산합니다.  

    4️⃣ **Recommendation**  
    └ 현재 소비 패턴을 바탕으로 탄소 배출량을 줄일 수 있는 개선 방향을 제시합니다.
    """
)

st.markdown("---")

tab = st.tabs(["📚 데이터 및 탄소 배출 계수 출처 / EcoScore 계산 기준"])[0]

with tab:
    st.markdown(
        """
        본 프로젝트에서 사용하는 탄소 배출 계수(kg CO₂e)는  
        신뢰할 수 있는 공공 데이터 및 관련 문헌을 참고하여 설정하였습니다.  
    
        구체적인 카테고리별 배출 계수와 상세 출처, EcoScore 계산 기준은  
        좌측의 **Source** 페이지와 README 파일에서 확인할 수 있습니다.
        """
    )

st.markdown("---")

st.markdown(
    """
    <small>
    EcoBudget Pro는 개인 소비 데이터에 기반한 탄소 발자국을 분석해    
    일상 속에서 실천 가능한 친환경 소비를 돕는 것을 목표로 합니다.
    </small>
    """,
    unsafe_allow_html=True,
)