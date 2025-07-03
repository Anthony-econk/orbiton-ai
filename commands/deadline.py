# commands/deadline.py
from fastapi.responses import PlainTextResponse
from services.clickup import create_clickup_task, find_similar_task  # ✅ 유사도 함수 추가
from datetime import datetime


# /orbiton.deadline 명령어 처리 핸들러
# 입력 예시: "/orbiton.deadline 업무제출 2025-07-10"
# 유사도 검색 패턴 추가하여 기존 소스 수정 2025-07-03    
async def handle(text, user_name):
    try:
        task_raw, due_str = text.strip().rsplit(" ",1)
        full_name = f"{user_name}: {task_raw.strip()}"
        due_ts = int(datetime.strptime(due_str, "%Y-%m-%d").timestamp()*1000)

        similar = find_similar_task(full_name)
        if similar:
            top_id, top_name, score = similar[0]
            return PlainTextResponse(
                f"⚠️ 유사한 작업이 있습니다 ({score:.0f}% 유사): *{top_name}*\n"
                f"• ✅ 기존 작업에 마감일을 적용하시겠습니까?\n"
                f"• ❌ 새 작업 생성하시겠습니까?"
            )
        else:
            result = create_clickup_task(full_name, due_date=due_ts)
            return PlainTextResponse("생성" if result.get("id") else "생성 실패")

    except Exception as e:
        return PlainTextResponse(f"❌ 입력 오류 또는 형식을 확인해주세요: {e}")
    
    #동일 소스 재배포를 위해 주석 남김
