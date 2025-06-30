from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.post("/slack/events")
async def slack_events(request: Request):
    form_data = await request.form()
    command = form_data.get("command")  # ex. "/orbiton.assign"
    text = form_data.get("text")        # ex. "@techsoft 보고서 작성"
    user_name = form_data.get("user_name")

    print(f"📩 Received: {command=} {text=} {user_name=}")

    # 명령어 종류에 따라 분기
    if command == "/orbiton.assign":
        return PlainTextResponse(f"✔ Task assigned: {text}")
    elif command == "/orbiton.deadline":
        return PlainTextResponse(f"📆 Deadline set: {text}")
    elif command == "/orbiton.list":
        return PlainTextResponse("📝 Here's your task list!")
    elif command == "/orbiton.delete":
        return PlainTextResponse(f"❌ Deleted task: {text}")
    else:
        return PlainTextResponse(f"❓ Unknown command: {text}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
