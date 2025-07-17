# app/commands/slack/deadline.py
# Slack 명령어 /orbiton.deadline 처리 - ClickUp 태스크 마감일 설정

from app.services import clickup_service

# /orbiton.deadline 명령어를 처리하여 태스크의 마감일을 설정
async def handle_deadline_command(list_id: str, task_name: str, deadline: str) -> str:
    # 리스트에서 태스크 목록 조회
    tasks = await clickup_service.get_tasks_from_list(list_id)

    # 태스크명으로 대상 태스크 찾기
    target_task = next((task for task in tasks if task.get('name') == task_name), None)
    if not target_task:
        return f"'{task_name}'이라는 이름의 태스크를 찾을 수 없습니다."

    task_id = target_task.get('id')

    # 기존 마감일 확인
    current_deadline = target_task.get('due_date', None)
    if current_deadline == deadline:
        return f"'{task_name}' 태스크는 이미 지정된 마감일이 {deadline}입니다."

    # ClickUp API를 통해 마감일 설정
    result = await clickup_service.set_deadline(task_id, deadline)

    if result:
        return f"'{task_name}' 태스크의 마감일이 {deadline}(으)로 설정되었습니다."
    else:
        return f"'{task_name}' 태스크의 마감일 설정에 실패했습니다."