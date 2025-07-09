# commands/delete.py
from fastapi.responses import PlainTextResponse
from services.clickup import delete_task_by_id, find_similar_task, add_task_comment

# /orbiton.delete 명령어 핸들러
async def handle(text, user_name):
    try:
        task_name = text.strip()
        if not task_name:
            return PlainTextResponse("❌ 작업명을 입력해주세요.")

        # 유사한 작업 찾기
        similar = find_similar_task(task_name)
        if similar:
            top_id, top_name, score = similar[0]

            if score >= 80:
                success = delete_task_by_id(top_id)

                # 코멘트 남기기
                comment = f"❌ *{user_name}*님이 이 작업을 삭제했습니다: {top_name}"
                add_task_comment(top_id, comment)

                return PlainTextResponse(
                    f"❌ 삭제 완료: {top_name}" if success else "⚠️ 삭제 실패"
                )
            else:
                return PlainTextResponse(
                    f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): {top_name}"
                )
        else:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_name}")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
