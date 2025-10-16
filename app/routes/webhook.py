from fastapi import APIRouter, Request
from app.utils.lyzr_client import query_lyzr

router = APIRouter()

@router.post("/input")
async def handle_webhook(request: Request):
    payload = await request.json()
    user_message = payload.get("text", "")
    lyzr_response = await query_lyzr(user_message)
    return {"reply": lyzr_response}
