def eco_score(total_carbon: float) -> float:
    """
    총 탄소 배출량(kg CO2e)을 0~100점 친환경 점수로 변환
    """
    if total_carbon <= 20:
        return 100.0
    elif total_carbon <= 50:
        return round(100 - (total_carbon - 20) * 1.3, 1)
    else:
        return max(0.0, round(60 - (total_carbon - 50) * 0.8, 1))
