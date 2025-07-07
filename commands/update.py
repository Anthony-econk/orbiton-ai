# commands/update.py
from fastapi.responses import PlainTextResponse
from services.clickup import update_task_description, find_similar_task
import re

# /orbiton.update 명령어 핸들러
async def handle(text, user_name):
    try:
        # 입력 예: "회의자료 정리 중요한 회의 안건 포함"
        parts = text.strip().split(" ", 1)
        if len(parts) != 2:
            return PlainTextResponse("❌ 입력 형식 오류: [작업명] [설명] 형식으로 입력해주세요.")

        task_name_raw, description = parts
        full_name = f"{user_name}: {task_name_raw.strip()}"

        similar = find_similar_task(full_name)
        if not similar:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name_raw}")

        task_id, task_name, score = similar[0]
        if score < 90:
            return PlainTextResponse(
                f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): *{task_name}*"
            )

        success = update_task_description(task_id, description)
        if success:
            return PlainTextResponse(f"✏️ 작업 설명 수정 완료: {task_name_raw}")
        else:
            return PlainTextResponse("❌ 설명 수정 실패")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
