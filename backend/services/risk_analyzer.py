# app/services/risk_analyzer.py
# 프로젝트 리스크 분석 서비스 모듈

from typing import List, Dict

# 예시 리스크 점수 기준 (향후 ML 모델로 확장 가능)
RISK_KEYWORDS = {
    "지연": 10,
    "병목": 15,
    "인력 부족": 20,
    "기술적 어려움": 25,
    "요구사항 변경": 15
}

# 작업 리스트에서 리스크 점수를 계산하여 반환
def analyze_risks(tasks: List[Dict]) -> List[Dict]:
    analyzed = []
    for task in tasks:
        risk_score = 0
        description = task.get("description", "")

        for keyword, score in RISK_KEYWORDS.items():
            if keyword in description:
                risk_score += score

        analyzed.append({
            "task_id": task.get("id"),
            "name": task.get("name"),
            "risk_score": risk_score,
            "description": description
        })

    return analyzed

# 리스크가 높은 작업만 필터링
def high_risk_tasks(analyzed_tasks: List[Dict], threshold: int = 20) -> List[Dict]:
    return [task for task in analyzed_tasks if task["risk_score"] >= threshold]