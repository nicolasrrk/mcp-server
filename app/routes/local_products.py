import os
import json
from fastapi import APIRouter, Query
from typing import List

router = APIRouter()
DATA_DIR = "app/data"  # ajustá si tu carpeta 'data' está en otro lugar
CHUNK_PREFIX = "products_"

def normalize_text(text: str) -> str:
    """Convierte texto a minúsculas y elimina acentos para mejor coincidencia."""
    import unicodedata
    if not isinstance(text, str):
        text = str(text)
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

@router.get("/search")
async def search_local_products(
    query: str = Query(..., description="Texto a buscar (por nombre, marca, categoría, etc.)"),
    page: int = Query(1, description="Número de página"),
    per_page: int = Query(50, description="Resultados por página")
):
    """Busca productos localmente en los JSON generados desde el CSV por lotes."""
    query_norm = normalize_text(query)
    results: List[dict] = []

    chunk_files = sorted([
        f for f in os.listdir(DATA_DIR)
        if f.startswith(CHUNK_PREFIX) and f.endswith(".json")
    ])

    for chunk_path in chunk_files:
        with open(os.path.join(DATA_DIR, chunk_path), "r", encoding="utf-8") as f:
            chunk = json.load(f)

        for product in chunk:
            # buscamos en los campos relevantes del CSV
            texto_busqueda = " ".join([
                str(product.get("Nombre", "")),
                str(product.get("Marca", "")),
                str(product.get("Categoría", "")),
                str(product.get("Color", "")),
                str(product.get("Talle", "")),
                str(product.get("ID", "")),
            ])
            texto_norm = normalize_text(texto_busqueda)

            if query_norm in texto_norm:
                results.append({
                    "id": product.get("ID"),
                    "name": product.get("Nombre"),
                    "brand": product.get("Marca"),
                    "category": product.get("Categoría"),
                    "color": product.get("Color"),
                    "size": product.get("Talle"),
                    "stock": product.get("Stock"),
                    "price": product.get("Precio"),
                    "url": product.get("URL"),
                    "image": product.get("Imagen"),
                })

        # Si ya superamos un límite de resultados (p. ej. 1000), paramos para no saturar memoria
        if len(results) > 1000:
            break

    # === Paginación ===
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    page_results = results[start:end]

    return {
        "query": query,
        "page": page,
        "results_count": len(page_results),
        "total_found": total,
        "has_more": end < total,
        "products": page_results
    }
