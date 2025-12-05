import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualization - EcoBudget Pro", page_icon="📊")

st.title("📊 Visualization")
st.caption("카테고리별 소비 및 탄소 배출량 시각화")

st.markdown("---")

if "df" not in st.session_state:
    st.warning("먼저 **Upload Data** 페이지에서 CSV 파일을 업로드해 주세요.")
    st.stop()

df: pd.DataFrame = st.session_state["df"]

st.subheader("현재 데이터")
st.markdown(f"- 총 행 개수: **{len(df)}**")
st.dataframe(df, use_container_width=True)

try:
    category_summary = (
        df.groupby("category")["carbon_kg"]
        .sum()
        .reset_index()
        .sort_values(by="carbon_kg", ascending=False)
    )
except Exception as e:
    st.error(f"카테고리별 탄소 배출량을 계산하는 중 오류가 발생했습니다: {e}")
    st.stop()

category_summary.insert(0, "순위", range(1, len(category_summary) + 1))

display_summary = category_summary.rename(
    columns={
        "순위": "순위",
        "category": "카테고리",
        "carbon_kg": "탄소 배출량(kg CO₂e)",
    }
)

display_summary["탄소 배출량(kg CO₂e)"] = (
    display_summary["탄소 배출량(kg CO₂e)"].round(3)
)

st.markdown("---")

st.subheader("카테고리별 탄소 배출량 요약(내림차순)")
st.markdown("단위: **kg CO₂e**")

def highlight_top3(row):
    rank = row["순위"]
    styles = []
    for col in row.index:
        if col == "탄소 배출량(kg CO₂e)":
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
            "순위": st.column_config.NumberColumn("순위", width="xx-small", format="%d"),
            "카테고리": st.column_config.TextColumn("카테고리", width="medium"),
            "탄소 배출량(kg CO₂e)": st.column_config.NumberColumn(
                "탄소 배출량(kg CO₂e)", width="small", format="%.3f"
            ),
        },
    )

try:
    fig_bar = px.bar(
        category_summary,
        x="category",
        y="carbon_kg",
        text_auto=".2f",
        title="카테고리별 탄소 배출량(kg CO₂e)",
    )
    fig_bar.update_layout(xaxis_title="카테고리", yaxis_title="탄소 배출량(kg CO₂e)")
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_pie = px.pie(
        category_summary,
        names="category",
        values="carbon_kg",
        title="카테고리별 탄소 배출 비율",
    )
    st.plotly_chart(fig_pie, use_container_width=True)
except Exception as e:
    st.error(f"그래프를 생성하는 중 오류가 발생했습니다: {e}")
    st.stop()

st.success("✅ 시각화 완료")