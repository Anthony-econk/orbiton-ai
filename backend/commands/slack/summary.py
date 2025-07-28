# backend/commands/slack/summary.py
# Slack 명령어 /orbiton.summary 처리 - ClickUp 태스크 목록 요약 및 LLaMA 호출

from fastapi.responses import PlainTextResponse
from backend.services import clickup_service, llama_service
from backend.prompts import prompts  # ✅ 경로 수정

# /orbiton.summary 명령어를 처리하여 태스크 목록 요약 반환
async def handle_summary_command(list_id: str) -> PlainTextResponse:
    try:
        tasks = await clickup_service.get_tasks_from_list(list_id)

        if not tasks:
            return PlainTextResponse("❌ 현재 등록된 태스크가 없습니다.")

        task_titles = await clickup_service.extract_task_titles(tasks)
        prompt = prompts.build_project_summary_prompt(task_titles)
        summary = await llama_service.query_llama(prompt)

        return PlainTextResponse("🗒️ *프로젝트 요약:*\n" + summary)

    except Exception as e:
        return PlainTextResponse(f"❌ 요약 처리 중 오류 발생: {e}")
