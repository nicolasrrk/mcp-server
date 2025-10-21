from fastapi import APIRouter, Request
from app.utils.lyzr_client import query_lyzr

router = APIRouter()

@router.post("/input")
async def handle_webhook(request: Request):
    """
    Endpoint de entrada para recibir mensajes de LucidBot (u otros clientes).
    Envía el mensaje al modelo Lyzr y devuelve una respuesta legible.
    """
    try:
        payload = await request.json()
        user_message = payload.get("text", "")

        if not user_message:
            return {"error": "No se recibió texto en la solicitud."}

        # Llama al cliente Lyzr
        lyzr_response = await query_lyzr(user_message)

        # Procesa y extrae texto legible
        reply_text = ""
        if isinstance(lyzr_response, dict):
            try:
                reply_text = (
                    lyzr_response.get("output", [{}])[0]
                    .get("content", [{}])[0]
                    .get("text", "")
                )
            except (KeyError, IndexError, TypeError):
                reply_text = str(lyzr_response)
        else:
            reply_text = str(lyzr_response)

        return {"reply": reply_text}

    except Exception as e:
        return {"error": f"Ocurrió un error procesando el webhook: {str(e)}"}
