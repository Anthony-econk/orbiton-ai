from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

@app.post("/slack/events")
async def slack_events(request: Request):
    payload = await request.json()
    print("Received event:", payload)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
