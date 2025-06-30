from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

@app.post("/slack/events")
async def slack_events(request: Request, x_slack_signature: str = Header(None), x_slack_request_timestamp: str = Header(None)):
    payload = await request.json()
    
    # ✅ Slack Challenge 처리 (URL 검증용)
    if payload.get("type") == "url_verification":
        return JSONResponse(content={"challenge": payload["challenge"]})

    # ✅ Slack Event 처리 로그
    print("🔔 Event received from Slack:", payload)

    return JSONResponse(content={"ok": True})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
