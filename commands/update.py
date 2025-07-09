# commands/update.py
from fastapi.responses import PlainTextResponse
from services.clickup import update_task_description, find_similar_task, add_task_comment
import re

# /orbiton.update 명령어 핸들러
async def handle(text, user_name):
    try:
        # 입력 예: "회의자료 정리 중요한 회의 안건 포함"
        task_name, description = text.strip().split(" ", 1)

        # 기존 작업 중 유사한 것 찾기
        similar = find_similar_task(task_name)

        if similar:
            top_id, top_name, score = similar[0]
            if score >= 80:
                success = update_task_description(top_id, description)

                # 🗨️ 자동 댓글 추가
                comment = f"✏️ *{user_name}*님이 Slack을 통해 작업 설명을 변경했습니다:\n> {description}"
                add_task_comment(top_id, comment)
                
                
                return PlainTextResponse(
                    f"✏️ 작업 설명 수정 완료: {top_name}" if success else "⚠️ 설명 수정 실패"
                )
            else:
                return PlainTextResponse(
                    f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): {top_name}"
                )
        else:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

    except Exception as e:
        return PlainTextResponse(f"❌ 입력 오류 또는 형식을 확인해주세요: {e}")