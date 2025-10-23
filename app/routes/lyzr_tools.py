from fastapi import APIRouter
from app.utils.lyzr_client import query_lyzr

router = APIRouter()

# === Chat con Lyzr ===
@router.post("/chat")
async def chat_with_lyzr(data: dict):
    message = data.get("message", "")
    response = await query_lyzr(message)
    return {"response": response}

# === Definición de herramientas MCP ===
tools = [
    {
        "name": "get_all_products",
        "description": "Devuelve todos los productos de la Tienda Nube con paginación interna.",
        "endpoint": "/tiendanube/all-products",
        "method": "GET",
        "params": {}
    },
    {
        "name": "get_categories",
        "description": "Obtiene todas las categorías disponibles.",
        "endpoint": "/tiendanube/categories",
        "method": "GET",
        "params": {}
    }
]

# === Endpoint para que LucidBot lea las herramientas ===
@router.get("/tools")
def list_tools():
    return {
        "mcp_version": "1.0",
        "tools": tools
    }
