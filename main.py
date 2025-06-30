from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.post("/slack/events")
async def slack_events(request: Request):
    form_data = await request.form()
    command = form_data.get("command")
    text = form_data.get("text")
    user_name = form_data.get("user_name")

    print(f"📩 Received: {command=} {text=} {user_name=}")

    # 실제 메시지를 슬랙에 출력하도록 응답 본문 리턴
    if text.startswith("assign"):
        return PlainTextResponse(f"✔ Assigned task to {user_name}: {text}")
    elif text.startswith("deadline"):
        return PlainTextResponse(f"📆 Deadline registered: {text}")
    elif text.startswith("list"):
        return PlainTextResponse("📝 Here’s your task list!\n- Task 1\n- Task 2")
    else:
        return PlainTextResponse(f"❓ Unknown command: `{text}`")
