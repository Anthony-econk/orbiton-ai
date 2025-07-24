# app/commands/slack/delete.py
# Slack 명령어 /orbiton.delete 처리 - ClickUp 태스크 삭제 및 자동 코멘트

from fastapi.responses import PlainTextResponse
from backend.services import clickup_service

# /orbiton.delete 명령어를 처리하여 태스크 삭제 및 코멘트 기록
async def handle_delete_command(list_id: str, text: str, user_name: str) -> PlainTextResponse:
    try:
        task_name = text.strip()
        if not task_name:
            return PlainTextResponse("❌ 삭제할 태스크명을 입력해주세요.")

        # 기존 작업 중 유사한 것 찾기
        similar = await clickup_service.find_similar_task(list_id, task_name)

        if similar:
            top_task = similar[0]
            task_id = top_task['id']
            top_name = top_task['name']
            score = top_task['score']

            if score >= 80:
                success = await clickup_service.delete_task(task_id)

                if success:
                    # 삭제 전 코멘트 남기기
                    comment = f"🗑️ *{user_name}*님이 Slack을 통해 이 작업을 삭제했습니다."
                    await clickup_service.add_task_comment(task_id, comment)

                    return PlainTextResponse(f"🗑️ 작업 삭제 완료: {top_name}")
                else:
                    return PlainTextResponse("⚠️ 작업 삭제에 실패했습니다.")
            else:
                return PlainTextResponse(f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): {top_name}")
        else:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")