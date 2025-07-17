# app/commands/slack/update.py
# Slack 명령어 /orbiton.update 처리 - ClickUp 태스크 내용 업데이트 및 자동 코멘트

from fastapi.responses import PlainTextResponse
from app.services import clickup_service
import re

# /orbiton.update 명령어를 처리하여 태스크의 내용을 업데이트하고 코멘트 추가
async def handle_update_command(list_id: str, text: str, user_name: str) -> PlainTextResponse:
    try:
        # 입력 형식: "태스크명 설명"
        split_text = text.strip().split(" ", 1)
        if len(split_text) != 2:
            return PlainTextResponse("❌ 입력 형식 오류: '태스크명 설명' 형식으로 입력해주세요.")

        task_name, new_description = split_text

        # 기존 작업 중 유사한 것 찾기
        similar = await clickup_service.find_similar_task(list_id, task_name)

        if similar:
            top_task = similar[0]
            task_id = top_task['id']
            top_name = top_task['name']
            score = top_task['score']

            if score >= 80:
                success = await clickup_service.update_task_content(task_id, new_description)

                # 자동 댓글 추가
                comment = f"✏️ *{user_name}*님이 Slack에서 작업 설명을 수정했습니다:\n> {new_description}"
                await clickup_service.add_task_comment(task_id, comment)

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
        return PlainTextResponse(f"❌ 오류 발생: {e}")