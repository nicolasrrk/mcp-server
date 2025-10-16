from fastapi import APIRouter
from app.utils.lyzr_client import query_lyzr

router = APIRouter()

@router.post("/chat")
async def chat_with_lyzr(data: dict):
    message = data.get("message", "")
    response = await query_lyzr(message)
    return {"response": response}
