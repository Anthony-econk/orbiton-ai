# commands/status.py
from fastapi.responses import PlainTextResponse
from services.clickup import update_task_status, find_similar_task, add_task_comment

STATUS_MAP = {
    "완료": "done",
    "진행중": "in progress",
    "대기": "to do",
    "보류": "on hold"
}

# /orbiton.status 명령어 처리 핸들러
# 예시: /orbiton.status 보고서작성 done
async def handle(text, user_name):
    try:
                # 예: "사업계획서 완료"
        task_part, status_part = text.strip().rsplit(" ", 1)
        status = STATUS_MAP.get(status_part)

        if not status:
            return PlainTextResponse(
                f"❌ 상태 입력이 잘못되었습니다: {status_part}\n"
                f"사용 예: 완료, 진행중, 대기, 보류"
            )

# 유사도 찾기 부분    
        similar = find_similar_task(task_part)
        if similar:
            top_id, top_name, score = similar[0]
            if score >= 80:
                success = update_task_status(top_id, status)

                # 코멘트 추가
                comment = f"🔄 *{user_name}*님이 작업 상태를 변경했습니다 → *{status_part}*"
                add_task_comment(top_id, comment)

                return PlainTextResponse(
                    f"🔄 상태 변경 완료: {top_name} → {status_part}" if success else "⚠️ 상태 변경 실패"
                )
            else:
                return PlainTextResponse(
                    f"⚠️ 유사한 작업이 있지만 확실하지 않습니다 ({score:.0f}%): {top_name}"
                )
        else:
            return PlainTextResponse(f"❌ 작업을 찾을 수 없습니다: {task_part}")
    except Exception as e:
        return PlainTextResponse(f"❌ 입력 오류 또는 형식을 확인해주세요: {e}")

