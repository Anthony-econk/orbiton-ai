# backend/commands/slack/tasklist.py
# Slack 명령어 /orbiton.tasklist 처리 - ClickUp 태스크 목록 조회

from fastapi.responses import PlainTextResponse
from backend.services import clickup_service

# /orbiton.tasklist 명령어를 처리하여 전체 태스크 목록을 Slack에 반환
async def handle_tasklist_command(list_id: str) -> PlainTextResponse:
    try:
        tasks = await clickup_service.get_tasks_from_list(list_id)

        if not tasks:
            return PlainTextResponse("❌ 현재 등록된 태스크가 없습니다.")

        task_lines = []
        for task in tasks:
            task_name = task.get('name', '제목 없음')
            status = task.get('status', {}).get('status', '없음')
            assignees = ", ".join([a.get('username', '알 수 없음') for a in task.get('assignees', [])])
            task_lines.append(f"- {task_name} (상태: {status}, 담당자: {assignees if assignees else '없음'})")

        return PlainTextResponse("*📋 프로젝트 태스크 목록:*\n" + "\n".join(task_lines))

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
