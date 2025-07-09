from fastapi.responses import PlainTextResponse
from services.clickup import create_clickup_task, load_user_mapping, find_similar_task

# /orbiton.assign 명령어 핸들러
# 예시: /orbiton.assign 요구사항 정의서 작성
async def handle(text, user_name):
    try:
        mapping = load_user_mapping()
        assignee_email = mapping.get(user_name)

        task_name = text.strip()

        similar = find_similar_task(task_name)
        if similar:
            top_id, top_name, score = similar[0]
            if score >= 90:
                return PlainTextResponse(f"⚠️ 동일하거나 유사한 작업이 이미 있습니다: {top_name}")
        
        result = create_clickup_task(task_name, assignee_email=assignee_email)
        return PlainTextResponse(
            f"✔ 작업 생성됨: {task_name}" if result.get("id") else "⚠️ 생성 실패"
        )
    except Exception as e:
        return PlainTextResponse(f"❌ 오류: {e}")
