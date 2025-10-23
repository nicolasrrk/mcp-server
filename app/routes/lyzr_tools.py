from fastapi import APIRouter
from app.utils.lyzr_client import query_lyzr
import httpx

router = APIRouter()

# === Chat con Lyzr ===
@router.post("/chat")
async def chat_with_lyzr(data: dict):
    message = data.get("message", "")
    response = await query_lyzr(message)
    return {"response": response}

# === 🔁 Nueva función: obtener productos paginando ===
@router.get("/tiendanube/all-products")
async def get_all_products(page: int = 1, per_page: int = 100):
    """
    Devuelve todos los productos de Tienda Nube paginando automáticamente.
    Recorre todas las páginas hasta obtener todos los productos o un límite razonable.
    """
    base_url = "https://api.tiendanube.com/v1/products"  # cambia si usás tu endpoint interno
    headers = {
        "Authentication": "Bearer <TU_TOKEN_TIENDANUBE>",
        "Content-Type": "application/json",
    }

    all_products = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            params = {"page": page, "per_page": per_page}
            response = await client.get(base_url, headers=headers, params=params)

            if response.status_code != 200:
                break

            data = response.json()
            products = data if isinstance(data, list) else data.get("products", [])
            if not products:
                break

            all_products.extend(products)

            # Si la cantidad de productos es menor al límite, no hay más páginas
            if len(products) < per_page:
                break

            page += 1

            # 🔒 Evitamos saturar el servidor (por ejemplo, 1000 productos máximo)
            if len(all_products) >= 1000:
                break

    return {"count": len(all_products), "products": all_products}

# === Nueva herramienta para Lyzr ===
tools = [
    {
        "name": "get_all_products",
        "description": "Devuelve todos los productos de la Tienda Nube, paginando automáticamente hasta 1000 productos.",
        "endpoint": "/tiendanube/all-products",
        "method": "GET",
        "params": {
            "page": {"type": "int", "default": 1, "description": "Número de página inicial"},
            "per_page": {"type": "int", "default": 100, "description": "Cantidad de productos por página"},
        },
    },
    {
        "name": "get_categories",
        "description": "Obtiene todas las categorías disponibles.",
        "endpoint": "/tiendanube/categories",
        "method": "GET",
        "params": {},
    }
]

# === Endpoint para que LucidBot lea las herramientas ===
@router.get("/tools")
def list_tools():
    return {
        "mcp_version": "1.0",
        "tools": tools
    }
