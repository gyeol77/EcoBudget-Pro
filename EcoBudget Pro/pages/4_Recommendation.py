import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(page_title="Recommendation - EcoBudget Pro", page_icon="💡")

st.title("💡 개선 추천")
st.caption("탄소 배출량 상위 카테고리를 기반으로 소비 패턴 개선 방향과 절감 효과를 제시합니다.")

st.markdown("---")


if "df" not in st.session_state:
    st.warning("먼저 **데이터 업로드** 페이지에서 CSV 파일을 업로드해 주세요.")
    st.stop()

df: pd.DataFrame = st.session_state["df"]

if df.empty:
    st.warning("업로드된 데이터가 비어 있습니다.")
    st.stop()

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from utils.scoring import eco_score
except Exception as e:
    st.error(f"EcoScore 계산 함수를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

def grade_from_score(s: float) -> str:
    if s >= 70:
        return "A"
    elif s >= 50:
        return "B"
    elif s >= 30:
        return "C"
    else:
        return "D"

total_carbon = float(df["carbon_kg"].sum())
current_score = float(eco_score(total_carbon))
current_grade = grade_from_score(current_score)


st.subheader("절감 시나리오 설정")

reduction_percent = st.slider(
    "상위 카테고리 소비를 얼마나 줄인다고 가정할까요?",
    min_value=5,
    max_value=30,
    value=10,
    step=5,
    format="%d%%",
)

reduction_ratio = reduction_percent / 100.0

st.markdown(
    f"현재 전체 EcoScore는 **{current_score:.1f}점 (등급 {current_grade})** 입니다.  \n"
    f"아래에서는 배출량 상위 카테고리를 **{reduction_percent}%** 줄였을 때의 변화를 가정합니다."
)

st.markdown("---")

category_summary = (
    df.groupby("category")["carbon_kg"]
    .sum()
    .reset_index()
    .sort_values(by="carbon_kg", ascending=False)
)

category_summary.insert(0, "순위", range(1, len(category_summary) + 1))
category_summary["ratio"] = (category_summary["carbon_kg"] / total_carbon * 100).round(1)

display_df = category_summary.rename(
    columns={
        "category": "카테고리",
        "carbon_kg": "탄소 배출량(kg CO₂e)",
        "ratio": "비율(%)",
    }
)

display_df["reduction_kg"] = (display_df["탄소 배출량(kg CO₂e)"] * reduction_ratio).round(3)

top3 = display_df.head(3)


def highlight_top3(row):
    rank = row["순위"]
    styles = []
    for col in row.index:
        if col in ("탄소 배출량(kg CO₂e)", "reduction_kg", "비율(%)"):
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

styled_top3 = top3.style.apply(highlight_top3, axis=1)

 
st.subheader(f"배출량 상위 카테고리 TOP 3 (소비 {reduction_percent}% 절감 가정)")

st.dataframe(
    styled_top3,
    hide_index=True,
    use_container_width=True,
    column_config={
        "순위": st.column_config.NumberColumn("순위", width="small"),
        "카테고리": st.column_config.TextColumn("카테고리", width="medium"),
        "탄소 배출량(kg CO₂e)": st.column_config.NumberColumn(
            "탄소 배출량(kg CO₂e)", width="small", format="%.3f"
        ),
        "reduction_kg": st.column_config.NumberColumn(
            f"{reduction_percent}% 절감 시 감축량(kg CO₂e)",
            width="small",
            format="%.3f",
        ),
        "비율(%)": st.column_config.NumberColumn("비율(%)", width="small", format="%.1f"),
    },
)

st.markdown(
    f"""
    ※ 위 표의 '{reduction_percent}% 절감 시 감축량'은 각 카테고리 소비를 {reduction_percent}% 줄인다고 가정했을 때  
    예상되는 탄소 배출 감소량(kg CO₂e)을 의미합니다.
    """
)

st.markdown("---")


st.subheader("카테고리별 개선 방향 및 절감 효과")
st.markdown("### 🔎 상위 카테고리별 맞춤 개선 안내")

# 환산 상수
CAR_CO2_PER_KM = 0.2      # 자동차 1km당 약 0.2 kg CO₂e
CO2_PER_KWH = 0.424       # 전기 1kWh당 약 0.424 kg CO₂e
TREE_CO2_YEAR = 22        # 나무 1그루 연간 흡수 CO₂량 (kg)

recommendations = {
    "패션/미용": "불필요한 소비를 줄이고, 중고·친환경 제품을 활용하면 배출량을 크게 줄일 수 있습니다.",
    "주거/공과금": "전기·가스 사용을 줄이는 것이 핵심입니다. 절전 모드 활용과 효율적인 냉난방 사용을 추천드립니다.",
    "의료/건강": "필수 지출이지만, 불필요한 약품 구매 및 과잉 보관을 줄이면 도움이 됩니다.",
    "전자기기": "가전제품의 교체 주기를 늘리고 중고 거래를 활용해 보세요.",
    "교육/자기계발": "종이 교재 사용을 줄이고 디지털 자료 활용 비중을 높이는 것을 권장합니다.",
    "식음료": "일회용품 대신 텀블러같은 다회용기를 사용하면 탄소 절감 효과가 큽니다.",
    "생활용품": "재사용 가능한 제품을 선택하고, 친환경 제품으로 대체해 보세요.",
    "문화/여가": "여가생활도 중요하지만, 불필요한 소비는 없는지 체크해 보세요.",
    "교통": "대중교통과 자전거나 도보를 활용해 차량 이용 빈도를 줄이는 것이 효과적입니다.",
    "기타": "소비 내역을 세부적으로 점검하여 불필요한 구매를 줄이는 것이 효과적입니다.",
}

for _, row in top3.iterrows():
    category = row["카테고리"]
    carbon = float(row["탄소 배출량(kg CO₂e)"])
    reduction = float(row["reduction_kg"])
    ratio = float(row["비율(%)"])

    # 환경 효과 환산
    km_saved = reduction / CAR_CO2_PER_KM if CAR_CO2_PER_KM > 0 else 0.0
    kwh_saved = reduction / CO2_PER_KWH if CO2_PER_KWH > 0 else 0.0
    trees_saved = reduction / TREE_CO2_YEAR if TREE_CO2_YEAR > 0 else 0.0

    new_total = max(total_carbon - reduction, 0.0)
    new_score = float(eco_score(new_total))
    new_grade = grade_from_score(new_score)

    st.info(
        f"**{category}**  \n"
        f"- 현재 탄소 배출량: **{carbon:.3f} kg CO₂e** (전체의 약 **{ratio:.1f}%**)  \n"
        f"- 이 카테고리 소비를 **{reduction_percent}%만 줄이면**, 약 **{reduction:.3f} kg CO₂e**를 감축할 수 있습니다.  \n\n"
        f"🌍 **환경적 효과 환산**  \n"
        f"🚗 자동차 약 **{km_saved:.1f} km** 주행량 절감  \n"
        f"🔌 전기 약 **{kwh_saved:.1f} kWh** 절감  \n"
        f"🌲 나무 **{trees_saved:.2f} 그루**가 1년 동안 흡수하는 탄소량과 동일  \n\n"
        f"📊 **EcoScore 변화 시뮬레이션**  \n"
        f"- 현재 EcoScore: **{current_score:.1f}점 (등급 {current_grade})**  \n"
        f"- '{category}'만 {reduction_percent}% 줄이면: **{new_score:.1f}점 (등급 {new_grade})**  \n\n"
        f"💡 개선 제안: {recommendations.get(category, '이 카테고리의 소비 패턴을 점검해 보시는 것을 권장드립니다.')}"
    )


    with st.expander(f"🔍 '{category}' 카테고리 세부 소비 내역 보기"):
        cat_df = df[df["category"] == category].copy()
        if cat_df.empty:
            st.write("해당 카테고리의 세부 소비 내역이 없습니다.")
        else:
            cat_df = cat_df.sort_values(by="date")
            detail_df = cat_df[["date", "item", "price", "carbon_kg"]].rename(
                columns={
                    "date": "날짜",
                    "item": "품목",
                    "price": "가격(원)",
                    "carbon_kg": "탄소 배출량(kg CO₂e)",
                }
            )
            st.dataframe(detail_df, use_container_width=True, hide_index=True)


total_reduction_top3 = float(top3["reduction_kg"].sum())
combined_total_carbon = max(total_carbon - total_reduction_top3, 0.0)
combined_score = float(eco_score(combined_total_carbon))
combined_grade = grade_from_score(combined_score)

reduction_percent_total = (
    (total_reduction_top3 / total_carbon) * 100 if total_carbon > 0 else 0.0
)

st.markdown("---")
st.subheader("상위 3개 카테고리를 동시에 절감했을 때")

st.info(
    f"- 상위 3개 카테고리를 각각 **{reduction_percent}%**씩 줄이면, "
    f"총 **{total_reduction_top3:.3f} kg CO₂e**(약 **{reduction_percent_total:.1f}%**)를 감축하게 됩니다.  \n"
    f"- 현재 EcoScore: **{current_score:.1f}점 (등급 {current_grade})**  \n"
    f"- 상위 3개 카테고리를 동시에 절감 시: **{combined_score:.1f}점 (등급 {combined_grade})**"
)

st.markdown("---")

st.markdown(
    """
    <small>
    위 환경 효과 및 EcoScore 변화는 단순화된 가정에 기반한 추정치이며,  
    실제 감축 효과는 개별 소비 품목과 사용 패턴에 따라 달라질 수 있습니다.
    </small>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.success("✅ 개선 방향 제안 완료")