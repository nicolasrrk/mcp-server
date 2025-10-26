from fastapi import APIRouter, Query
import pandas as pd
import os

router = APIRouter()

# 📍 Ruta absoluta al CSV
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "utils", "productos.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

# 🔹 Cargar CSV una sola vez en memoria
df = pd.read_csv(DATA_PATH)

@router.get("/search")
async def search_local_products(
    query: str = Query(..., description="Texto a buscar (por nombre, marca, color, talle, etc.)"),
    page: int = Query(1, description="Número de página (paginado)"),
    per_page: int = Query(50, description="Cantidad de resultados por página")
):
    keywords = [k.strip().lower() for k in query.split() if k.strip()]

    # 🔍 Filtro: busca coincidencias de todas las palabras clave en cualquier campo
    mask = df.apply(lambda row: all(k in " ".join(map(str, row)).lower() for k in keywords), axis=1)
    results = df[mask]

    # 🔹 Paginación
    start = (page - 1) * per_page
    end = start + per_page
    paginated = results.iloc[start:end].to_dict(orient="records")

    # 🔹 Respuesta formateada
    return {
        "query": query,
        "page": page,
        "results_count": len(paginated),
        "total_found": len(results),
        "has_more": len(results) > end,
        "products": paginated
    }
