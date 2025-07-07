    # commands/mytask.py
from fastapi.responses import PlainTextResponse
from services.clickup import get_task_list

# /orbiton.mytask 명령어 처리 핸들러
# 등록된 사용자(Task 이름 앞에 user_name 포함된 것만) 필터링
async def handle(text, user_name):
    try:
        data = get_task_list()
        tasks = data.get("tasks", [])

        # ✅ 사용자 이름으로 시작하는 Task만 필터링
        my_tasks = [t for t in tasks if t["name"].startswith(f"{user_name}:")]

        if not my_tasks:
            return PlainTextResponse(f"📭 {user_name}님에게 할당된 작업이 없습니다.")

        # Task 요약 리스트 만들기
        response_lines = [f"📌 {t['name'].replace(f'{user_name}:', '').strip()} - `{t['status']['status']}`"
                          for t in my_tasks]
        response_text = f"🧑‍💻 *{user_name}님의 현재 작업 목록:*\n" + "\n".join(response_lines)

        return PlainTextResponse(response_text)

    except Exception as e:
        return PlainTextResponse(f"❌ 작업 조회 중 오류 발생: {e}")
