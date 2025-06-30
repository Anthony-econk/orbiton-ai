from fastapi import FastAPI, Request 
app = FastAPI() 
@app.post("/slack/events") 
async def slack_events(request: Request): 
"    payload = await request.json()" 
"    print('Slack payload received:', payload)" 
"    return {'status': 'ok'}" 
