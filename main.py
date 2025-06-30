from fastapi import FastAPI, Request
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

    # 여기서 명령어별 로직 분기
    if text.startswith("assign"):
        return PlainTextResponse(f"✔ Task assigned: {text}")
    elif text.startswith("deadline"):
        return PlainTextResponse(f"📆 Deadline set: {text}")
    elif text.startswith("list"):
        return PlainTextResponse("📝 Here's your task list!")
    else:
        return PlainTextResponse(f"🔍 Unknown command: `{text}`")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
