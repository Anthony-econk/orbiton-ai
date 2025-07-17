# app/commands/slack/assign.py
# Slack 명령어 /orbiton.assign 처리 - ClickUp 태스크 담당자 지정

from fastapi.responses import PlainTextResponse
from app.services import clickup_service

# /orbiton.assign 명령어를 처리하여 태스크의 담당자를 지정하고 코멘트 기록
async def handle_assign_command(list_id: str, text: str, user_name: str) -> PlainTextResponse:
    try:
        # 입력 형식: "태스크명 담당자명"
        split_text = text.strip().split(" ", 1)
        if len(split_text) != 2:
            return PlainTextResponse("❌ 입력 형식 오류: '태스크명 담당자명' 형식으로 입력해주세요.")

        task_name, assignee_name = split_text

        # 유사한 태스크 찾기
        similar = await clickup_service.find_similar_task(list_id, task_name)

        if similar:
            top_task = similar[0]
            task_id = top_task['id']
            top_name = top_task['name']
            score = top_task['score']

            if score >= 80:
                success = await clickup_service.assign_task(task_id, assignee_name)

                if success:
                    comment = f"👤 *{user_name}*님이 Slack에서 담당자를 '{assignee_name}'으로 지정했습니다."
                    await clickup_service.add_task_comment(task_id, comment)
                    return PlainTextResponse(f"👤 담당자 지정 완료: {top_name} → {assignee_name}")
                else:
                    return PlainTextResponse("⚠️ 담당자 지정에 실패했습니다.")
            else:
                return PlainTextResponse(
                    f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): {top_name}"
                )
        else:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")