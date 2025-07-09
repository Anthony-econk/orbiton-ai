from fastapi.responses import PlainTextResponse
from services.clickup import delete_task_by_id, find_similar_task, add_task_comment

# /orbiton.delete 명령어 핸들러
async def handle(text, user_name):
    try:
        parts = text.strip().split(" ", 1)

        # 사용자가 yes/no 입력했는지 확인
        if parts[0].lower() in ["yes", "no"] and len(parts) > 1:
            confirm = parts[0].lower()
            task_name = parts[1].strip()

            if confirm == "no":
                return PlainTextResponse("🚫 삭제가 취소되었습니다.")

            # "yes"인 경우 삭제 진행
            similar = find_similar_task(task_name)
            if similar:
                top_id, top_name, score = similar[0]
                if score >= 80:
                    success = delete_task_by_id(top_id)
                    if success:
                        comment = f"🗑️ *{user_name}*님이 Slack을 통해 작업을 삭제했습니다."
                        add_task_comment(top_id, comment)
                        return PlainTextResponse(f"🗑️ 작업 삭제 완료: {top_name}")
                    else:
                        return PlainTextResponse("⚠️ 작업 삭제 실패")
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

        else:
            # 일반 삭제 요청 → 유사도 확인
            task_name = text.strip()
            similar = find_similar_task(task_name)
            if similar:
                top_id, top_name, score = similar[0]
                return PlainTextResponse(
                    f"⚠️ 유사한 작업이 있습니다 ({score:.0f}% 유사): *{top_name}*\n"
                    f"🗑️ 정말 삭제하시겠습니까? (yes / no)\n"
                    f"➡️ 삭제하시려면 `/orbiton.delete yes {task_name}` 를 입력해주세요."
                )
            else:
                return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
