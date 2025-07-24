# app/summaries/summary_handler.py
# 설명: ClickUp 태스크 목록을 요약하기 위한 LLaMA 호출 핸들러

import os
from backend.services import clickup_service
from backend.summaries import prompts
from backend.services import llama_service

CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")
if not CLICKUP_LIST_ID:
    raise EnvironmentError("CLICKUP_LIST_ID 환경변수가 설정되지 않았습니다.")

async def handle_summary() -> str:
    """
    ClickUp에서 태스크 목록을 가져와 LLaMA로 프로젝트 요약을 수행한다.

    Returns:
        str: 요약 결과 문자열
    """
    tasks = await clickup_service.get_tasks_from_list(CLICKUP_LIST_ID)

    if not tasks:
        return "ClickUp에서 가져온 태스크가 없습니다."

    task_titles = await clickup_service.extract_task_titles(tasks)
    prompt = prompts.build_project_summary_prompt(task_titles)
    summary = await llama_service.query_llama(prompt)

    return summary