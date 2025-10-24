from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

# Ruta absoluta a la carpeta /data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)


@router.get("/search")
async def search_local_products(
    query: str = Query(..., description="Texto a buscar (por nombre, marca, color, talle, etc.)"),
    page: int = Query(1, description="Número de página"),
    per_page: int = Query(50, description="Cantidad de resultados por página")
):
    keywords = [q.strip().lower() for q in query.split() if q.strip()]

    all_products = []

    # 🔹 Cargar todos los archivos JSON del directorio data/
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)

                    # Si el archivo es una cadena (texto JSON dentro de otro JSON)
                    if isinstance(data, str):
                        data = json.loads(data)

                    # Si no es lista, omitir
                    if not isinstance(data, list):
                        print(f"⚠️ Archivo {filename} no contiene una lista válida, se omite.")
                        continue

                    all_products.extend(data)

                except Exception as e:
                    print(f"❌ Error al leer {filename}: {e}")

    matched = []

    # 🔹 Buscar coincidencias
    for p in all_products:
        if not isinstance(p, dict):
            continue  # saltar si no es un diccionario

        text = " ".join([
            str(p.get("Nombre", "")),
            str(p.get("Marca", "")),
            str(p.get("Categoría", "")),
            str(p.get("Color", "")),
            str(p.get("Talle", "")),
            str(p.get("Stock", "")),
            str(p.get("Precio", "")),
        ]).lower()

        # Coincidencia: todas las palabras clave deben aparecer
        if all(k in text for k in keywords):
            matched.append(p)

    # 🔹 Paginación
    start = (page - 1) * per_page
    end = start + per_page
    paginated = matched[start:end]

    # 🔹 Respuesta final
    return {
        "query": query,
        "page": page,
        "results_count": len(paginated),
        "total_found": len(matched),
        "has_more": len(matched) > end,
        "products": paginated,
    }
