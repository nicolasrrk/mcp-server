from fastapi import APIRouter, HTTPException
import httpx
import os
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# === Configuración base ===
STORE_ID = os.getenv("TIENDANUBE_STORE_ID")
ACCESS_TOKEN = os.getenv("TIENDANUBE_ACCESS_TOKEN")
BASE_URL = f"https://api.tiendanube.com/v1/{STORE_ID}"

# === Cache en memoria (TTL en segundos, máx. 1 resultado almacenado) ===
CACHE_TTL = int(os.getenv("TIENDANUBE_CACHE_TTL", 600))
cache = TTLCache(maxsize=1, ttl=CACHE_TTL)


# === Función auxiliar ===
async def fetch_all_products():
    """
    Obtiene todos los productos de Tienda Nube recorriendo todas las páginas.
    """
    headers = {
        "Authentication": f"bearer {ACCESS_TOKEN}",
        "User-Agent": "Lyzr-TiendaNubeConnector (pampashop2025@gmail.com)"
    }

    all_products = []
    page = 1
    per_page = 200  # máximo permitido por la API

    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            params = {"page": page, "per_page": per_page}
            response = await client.get(f"{BASE_URL}/products", headers=headers, params=params)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            data = response.json()
            if not data:
                break

            all_products.extend(data)

            # Si devuelve menos de 200 productos, es la última página
            if len(data) < per_page:
                break

            page += 1

    return all_products


# === Endpoint para obtener productos ===
@router.get("/all-products")
async def get_all_products():
    """
    Endpoint para obtener todos los productos desde Tienda Nube.
    Usa caché para evitar sobrecarga de peticiones.
    """
    cache_key = "all_products"

    if cache_key in cache:
        return {
            "cached": True,
            "count": len(cache[cache_key]),
            "products": cache[cache_key]
        }

    products = await fetch_all_products()
    cache[cache_key] = products

    return {
        "cached": False,
        "count": len(products),
        "products": products
    }


@router.get("/categories")
async def get_categories():
    """
    Devuelve todas las categorías existentes de productos desde Tienda Nube,
    recorriendo todas las páginas y simplificando la respuesta.
    """
    headers = {
        "Authentication": f"bearer {ACCESS_TOKEN}",
        "User-Agent": "Lyzr-TiendaNubeConnector (pampashop2025@gmail.com)"
    }

    all_categories = []
    page = 1
    per_page = 200  # máximo permitido por la API

    async with httpx.AsyncClient(timeout=20.0) as client:
        while True:
            params = {"page": page, "per_page": per_page}
            response = await client.get(f"{BASE_URL}/categories", headers=headers, params=params)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            data = response.json()
            if not data:
                break

            # 🔽 Simplificamos los campos relevantes
            for c in data:
                simplified = {
                    "id": c.get("id"),
                    "name": c.get("name", {}).get("es", "") or c.get("name", {}).get("en", ""),
                    "description": c.get("description", {}).get("es", "") or c.get("description", {}).get("en", ""),
                    "parent_id": c.get("parent", {}).get("id") if c.get("parent") else None
                }
                all_categories.append(simplified)

            # Si devuelve menos que el máximo por página, no hay más
            if len(data) < per_page:
                break
            page += 1

    return {
        "count": len(all_categories),
        "categories": all_categories
    }


# === Endpoint de depuración de variables de entorno ===
@router.get("/tiendanube/debug")
async def debug_tiendanube():
    import os
    return {
        "store_id": os.getenv("TIENDANUBE_STORE_ID"),
        "access_token_exists": os.getenv("TIENDANUBE_ACCESS_TOKEN") is not None,
        "access_token_preview": (os.getenv("TIENDANUBE_ACCESS_TOKEN") or "")[:10] + "...",
        "cache_ttl": os.getenv("TIENDANUBE_CACHE_TTL"),
    }
