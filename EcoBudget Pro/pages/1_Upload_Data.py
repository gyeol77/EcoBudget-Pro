import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(page_title="Upload Data - EcoBudget Pro", page_icon="📥")

st.title("📥 Upload Data")
st.caption("소비 내역(영수증) CSV 파일 업로드 및 데이터 전처리")

st.markdown("---")

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from utils.carbon import add_category_and_carbon
except Exception as e:
    st.error(f"전처리 함수 로딩 중 오류가 발생했습니다: {e}")
    st.stop()

st.subheader("데이터 업로드")
st.markdown(
    """
    CSV 파일을 업로드하면 카테고리 분류 후 탄소 배출량이 계산됩니다.

    **필수 항목:**  
    - `date` (날짜)  
    - `item` (품목명)  
    - `price` (가격)
    """
)

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()

    required_cols = {"date", "item", "price"}

    if not required_cols.issubset(df.columns):
        st.error(
            f"업로드된 CSV에 필수 항목 {required_cols} 이(가) 모두 포함되어야 합니다."
        )
        st.stop()

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

    processed_df = add_category_and_carbon(df)

    st.session_state["raw_df"] = df
    st.session_state["df"] = processed_df

    st.subheader("📄 업로드된 데이터(전처리 결과)")
    st.dataframe(processed_df, use_container_width=True)

    st.success("✅ 데이터 업로드 및 전처리 완료")

else:
    st.info("데이터(CSV) 파일을 업로드하면 자동으로 전처리가 진행됩니다.")