import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(page_title="EcoScore - EcoBudget Pro", page_icon="🌱")

st.title("🌱 EcoScore")
st.caption("전체 탄소 배출량을 기반으로 한 친환경 점수")

st.markdown("---")

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from utils.scoring import eco_score
except Exception as e:
    st.error(f"EcoScore 계산 함수를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

if "df" not in st.session_state:
    st.warning("먼저 **Upload Data** 페이지에서 CSV 파일을 업로드해 주세요.")
    st.stop()

df: pd.DataFrame = st.session_state["df"]

if df.empty:
    st.warning("업로드된 데이터가 비어 있습니다.")
    st.stop()

total_carbon = float(df["carbon_kg"].sum())
total_carbon_rounded = round(total_carbon, 3)

score = eco_score(total_carbon)
score_rounded = round(score, 1)

if score_rounded >= 70:
    grade = "A"
elif score_rounded >= 50:
    grade = "B"
elif score_rounded >= 30:
    grade = "C"
else:
    grade = "D"


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("총 탄소 배출량(kg CO₂e)", f"{total_carbon_rounded:.3f}")

with col2:
    st.metric("나의 EcoScore", f"{score_rounded} / 100")

with col3:
    st.metric("등급", grade)

st.markdown("---")

try:
    category_summary = (
        df.groupby("category")["carbon_kg"]
        .sum()
        .reset_index()
        .sort_values(by="carbon_kg", ascending=False)
    )
except Exception as e:
    st.error(f"카테고리별 배출량을 계산하는 중 오류가 발생했습니다: {e}")
    st.stop()

category_summary.insert(0, "순위", range(1, len(category_summary) + 1))
category_summary["ratio"] = (
    category_summary["carbon_kg"] / total_carbon * 100
).round(1)

display_summary = category_summary.rename(
    columns={
        "순위": "순위",
        "category": "카테고리",
        "carbon_kg": "탄소 배출량(kg CO₂e)",
        "ratio": "비율(%)",
    }
)

st.subheader("카테고리별 탄소 배출 비율")

def highlight_top3(row):
    rank = row["순위"]
    styles = []
    for col in row.index:
        if col in ("탄소 배출량(kg CO₂e)", "비율(%)"):
            if rank == 1:
                styles.append("color: #ff4b4b; font-weight: 800;")  
            elif rank == 2:
                styles.append("color: #ff7f7f; font-weight: 700;")   
            elif rank == 3:
                styles.append("color: #ffb2b2; font-weight: 600;")   
            else:
                styles.append("")
        else:
            styles.append("")
    return styles

styled_summary = display_summary.style.apply(highlight_top3, axis=1)

left, _ = st.columns([4, 1])

with left:
    st.dataframe(
        styled_summary,
        hide_index=True,
        use_container_width=True,
        column_config={
            "순위": st.column_config.NumberColumn("순위", width="small"),
            "카테고리": st.column_config.TextColumn("카테고리", width="medium"),
            "탄소 배출량(kg CO₂e)": st.column_config.NumberColumn(
                "탄소 배출량(kg CO₂e)", width="small", format="%.3f"
            ),
            "비율(%)": st.column_config.NumberColumn(
                "비율(%)", width="small", format="%.1f"
            ),
        },
    )

if not category_summary.empty:
    top_category = category_summary.iloc[0]["category"]
else:
    top_category = None

st.markdown("")

if grade == "A":
    st.success(
        "전체적인 탄소 배출 수준이 매우 낮은 편입니다! "
        "현재 소비 패턴을 유지하시면 좋겠습니다. 🌍"
    )
elif grade == "B":
    st.success(
        "탄소 배출 수준이 비교적 양호한 편입니다. "
        f"**'{top_category}'** 카테고리에서 조금만 더 절감하시면 더 높은 점수를 기대할 수 있습니다. 🌱"
    )
elif grade == "C":
    st.warning(
        "전반적인 탄소 배출량이 다소 높은 편입니다. "
        f"우선 **'{top_category}'** 관련 소비를 줄이는 것부터 시작해 보시는 것을 권장합니다. 💡"
    )
else:
    st.error(
        "현재 탄소 배출량이 상당히 높은 편입니다. "
        f"**'{top_category}'** 카테고리 중심으로 소비 패턴을 조정하시면 "
        "EcoScore를 크게 개선하실 수 있습니다. 💪"
    )

st.markdown("---")


st.markdown(
    """
    <small>
    EcoScore는 전체 탄소 배출량을 기반으로 친환경 점수를 0 ~ 100점으로 정규화한 지표입니다.  
    탄소 배출량이 적을수록 높은 점수가 되도록 설계되어 있으며,  
    구체적인 환산 로직은 <code>utils/scoring.py</code>의 <code>eco_score()</code> 함수에 구현되어 있습니다.
    </small>
    """,
    unsafe_allow_html=True,
)