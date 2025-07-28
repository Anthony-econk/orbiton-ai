# backend/commands/slack/mytask.py
# Slack 명령어 /orbiton.mytask 처리 - 현재 사용자의 담당 태스크 목록 조회

from fastapi.responses import PlainTextResponse
from backend.services import clickup_service
from backend.utils.logger import logger


# 🔹 사용자 태스크 필터링 함수
def filter_user_tasks(tasks: list, slack_user_id: str) -> list:
    return [
        task for task in tasks
        if any(
            assignee.get('id') == slack_user_id
            for assignee in task.get('assignees', [])
        )
    ]


# 🔹 태스크 텍스트 포맷팅 함수
def format_task_lines(tasks: list) -> str:
    lines = []
    for task in tasks:
        name = task.get('name', '제목 없음')
        status = task.get('status', {}).get('status', '미정')
        due = task.get('due_date') or '마감일 없음'
        lines.append(f"• *{name}* _(상태: {status}, 마감일: {due})_")
    return "\n".join(lines)


# 🔹 /orbiton.mytask 명령 처리 핸들러
async def handle_mytask_command(list_id: str, slack_user_id: str) -> PlainTextResponse:
    try:
        tasks = await clickup_service.get_tasks_from_list(list_id)

        if not tasks:
            return PlainTextResponse("❌ 현재 등록된 태스크가 없습니다.")

        user_tasks = filter_user_tasks(tasks, slack_user_id)

        if not user_tasks:
            return PlainTextResponse("📭 현재 담당 중인 할 일이 없습니다.")

        message = "*🗒️ 담당 중인 태스크 목록:*\n" + format_task_lines(user_tasks)
        return PlainTextResponse(message)

    except Exception as e:
        logger.error(f"handle_mytask_command 오류: {e}")
        return PlainTextResponse("❌ 태스크 조회 중 오류가 발생했습니다.")
