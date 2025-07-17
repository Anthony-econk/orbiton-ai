# app/commands/slack/mytask.py
# Slack 명령어 /orbiton.mytask 처리 - 현재 사용자의 담당 태스크 목록 조회

from fastapi.responses import PlainTextResponse
from app.services import clickup_service

# /orbiton.mytask 명령어를 처리하여 사용자의 담당 태스크 목록 반환
async def handle_mytask_command(list_id: str, slack_user_id: str) -> PlainTextResponse:
    try:
        tasks = await clickup_service.get_tasks_from_list(list_id)

        if not tasks:
            return PlainTextResponse("❌ 현재 등록된 태스크가 없습니다.")

        user_tasks = [
            task for task in tasks
            if task.get('assignees') and any(assignee.get('id') == slack_user_id for assignee in task.get('assignees'))
        ]

        if not user_tasks:
            return PlainTextResponse("🔍 현재 담당 중인 할 일이 없습니다.")

        task_lines = []
        for task in user_tasks:
            task_name = task.get('name', '제목 없음')
            status = task.get('status', {}).get('status', '없음')
            due_date = task.get('due_date', '마감일 없음')
            task_lines.append(f"- {task_name} (상태: {status}, 마감일: {due_date})")

        return PlainTextResponse("*🗒️ 담당 할 일 목록:*\n" + "\n".join(task_lines))

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
