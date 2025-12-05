from .categorize import categorize_item

# kg CO2e / 10000원 기준
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


def calculate_carbon(price: float, category: str) -> float:
    """가격과 카테고리로 탄소 배출량(kg CO2e)을 계산"""
    factor = CARBON_FACTOR.get(category, 1.0)
    return round((price / 10000) * factor, 3)


def add_category_and_carbon(df):
    """DataFrame에 category, carbon_kg 컬럼을 추가해서 반환"""
    df = df.copy()
    df["item"] = df["item"].astype(str)
    df["category"] = df["item"].apply(categorize_item)
    df["price"] = df["price"].astype(float)
    df["carbon_kg"] = df.apply(
        lambda row: calculate_carbon(row["price"], row["category"]),
        axis=1,
    )
    return df