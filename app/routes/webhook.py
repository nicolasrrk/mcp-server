@router.post("/input")
async def handle_webhook(request: Request):
    payload = await request.json()
    user_message = payload.get("text", "")
    lyzr_response = await query_lyzr(user_message)
    
    # Extrae texto legible
    reply_text = ""
    if isinstance(lyzr_response, dict):
        try:
            reply_text = lyzr_response["output"][0]["content"][0]["text"]
        except (KeyError, IndexError, TypeError):
            reply_text = str(lyzr_response)
    
    return {"reply": reply_text}
