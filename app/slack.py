from fastapi import APIRouter, Request
from app.services.llama_service import parse_command
from app.commands import assign, deadline, delete, mytask, status, tasklist, update

router = APIRouter()

@router.post("/slack")
async def handle_slack_command(request: Request):
    data = await request.form()
    user_input = data.get("text", "")

    parsed_command = parse_command(user_input)

    if 'error' in parsed_command:
        return {"text": f"명령어 해석 실패: {parsed_command['error']}"}

    action = parsed_command.get("action")

    if action == "assign":
        result = assign.handle_assign(parsed_command)
    elif action == "deadline":
        result = deadline.handle_deadline(parsed_command)
    elif action == "delete":
        result = delete.handle_delete(parsed_command)
    elif action == "mytask":
        result = mytask.handle_mytask(parsed_command)
    elif action == "update":
        result = update.handle_update(parsed_command)
    elif action == "status":
        result = status.handle_status(parsed_command)
    elif action == "tasklist":
        result = tasklist.handle_tasklist(parsed_command)
    else:
        result = {"text": "알 수 없는 명령입니다."}

    return result
