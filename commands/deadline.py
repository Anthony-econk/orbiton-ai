# commands/deadline.py
from fastapi.responses import PlainTextResponse
from services.clickup import create_clickup_task
from datetime import datetime

# /orbiton.deadline 명령어 처리 핸들러
# 입력 예시: "/orbiton.deadline 업무제출 2025-07-10"
async def handle(text, user_name):
    try:
        # ✅ 입력 파싱: 작업명과 날짜를 분리 (공백 기준)
        parts = text.strip().split()
        if len(parts) != 2:
            raise ValueError("형식: [작업명] [YYYY-MM-DD] 예) 업무제출 2025-07-10")

        task_name, due_date_str = parts

        # ✅ 날짜 파싱 (문자열 → timestamp(ms))
        due_timestamp = int(datetime.strptime(due_date_str, "%Y-%m-%d").timestamp() * 1000)

        # ✅ 사용자명 포함한 작업 생성
        full_task_name = f"{user_name}: {task_name}"
        result = create_clickup_task(full_task_name, due_date=due_timestamp)

        if result.get("id"):
            return PlainTextResponse(f"📆 마감일 포함 작업 생성 완료: {task_name} (Due: {due_date_str})")
        else:
            return PlainTextResponse("⚠️ ClickUp Task 생성 실패")

    except Exception as e:
        return PlainTextResponse(f"❌ 입력 오류 또는 날짜 형식 오류: {str(e)}")