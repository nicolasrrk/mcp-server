from fastapi import APIRouter, Query, HTTPException
import os
import json
import httpx
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# === Configuración base ===
STORE_ID = os.getenv("TIENDANUBE_STORE_ID")
ACCESS_TOKEN = os.getenv("TIENDANUBE_ACCESS_TOKEN")
BASE_URL = f"https://api.tiendanube.com/v1/{STORE_ID}"

DATA_DIR = "app/data"  
CACHE_TTL = int(os.getenv("TIENDANUBE_CACHE_TTL", 600))
cache = TTLCache(maxsize=2, ttl=CACHE_TTL)

# === Endpoint local optimizado ===
@router.get("/products")
async def get_products(
    query: str = Query(None, description="Palabra clave para buscar productos"),
    page: int = Query(1, description="Número de página/lote"),
    per_page: int = Query(100, description="Cantidad de productos por lote")
):
    """
    Devuelve productos desde los archivos locales (JSON) por lotes.
    Si se pasa 'query', busca coincidencias por nombre o descripción.
    """

    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith("products_")])
    if not files:
        raise HTTPException(status_code=404, detail="No hay archivos de productos en la carpeta data.")

    if page > len(files):
        return {
            "query": query,
            "page": page,
            "results_count": 0,
            "has_more": False,
            "products": []
        }

    path = os.path.join(DATA_DIR, files[page - 1])
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if query:
        data = [
            p for p in data
            if query.lower() in str(p.get("Nombre", "")).lower()
            or query.lower() in str(p.get("Categoría", "")).lower()
        ]

    has_more = page < len(files)

    return {
        "query": query,
        "page": page,
        "results_count": len(data),
        "has_more": has_more,
        "products": [
            {
                "id": p.get("ID"),
                "name": p.get("Nombre"),
                "price": p.get("Precio"),
                "stock": p.get("Stock"),
                "category": p.get("Categoría"),
                "url": p.get("URL"),
                "image": p.get("Imagen")
            }
            for p in data[:per_page]
        ]
    }

# === Endpoint de categorías (sigue usando la API) ===
@router.get("/categories")
async def get_categories():
    headers = {
        "Authentication": f"{ACCESS_TOKEN}",
        "User-Agent": "Lyzr-TiendaNubeConnector (pampashop2025@gmail.com)"
    }

    all_categories = []
    page = 1
    per_page = 200

    async with httpx.AsyncClient(timeout=20.0) as client:
        while True:
            params = {"page": page, "per_page": per_page}
            response = await client.get(f"{BASE_URL}/categories", headers=headers, params=params)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            data = response.json()
            if not data:
                break

            for c in data:
                all_categories.append({
                    "id": c.get("id"),
                    "name": c.get("name", {}).get("es", "") or c.get("name", {}).get("en", ""),
                    "description": c.get("description", {}).get("es", "") or c.get("description", {}).get("en", "")
                })

            if len(data) < per_page:
                break
            page += 1

    return {"count": len(all_categories), "categories": all_categories}

# === Debug ===
@router.get("/debug")
async def debug_tiendanube():
    return {
        "store_id": STORE_ID,
        "access_token_exists": ACCESS_TOKEN is not None,
        "cache_ttl": CACHE_TTL,
        "data_dir_exists": os.path.exists(DATA_DIR),
        "local_files_count": len(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0
    }
