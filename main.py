# main.py
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from commands import assign, deadline, tasklist, delete, update, status, mytask
import uvicorn
import os
import requests

# FastAPI 앱 생성
app = FastAPI()

# Slack 명령어 요청 처리
@app.post("/slack/events")
async def slack_events(request: Request):
    form_data = await request.form()
    command = form_data.get("command")
    text = form_data.get("text")
    user_name = form_data.get("user_name")

    print(f"\U0001F4E9 Received: {command=} {text=} {user_name=}")
    # Clickup을 위한 분기 핸들러 적용
    if command == "/orbiton.assign":
        return await assign.handle(text, user_name)
    elif command == "/orbiton.deadline":
        return await deadline.handle(text, user_name)
    elif command == "/orbiton.list":
        return await tasklist.handle(text, user_name)
    elif command == "/orbiton.delete":
        return await delete.handle(text, user_name)
    elif command == "/orbiton.update":
        return await update.handle(text, user_name)
    elif command == "/orbiton.status":
        return await status.handle(text, user_name)
    elif command == "/orbiton.mytask":
        return await mytask.handle(text, user_name)
    else:
        return PlainTextResponse(f"❓ Unknown command: {text}")

# 로컬 실행용 진입점 (Render 배포 시 사용되지 않음)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
