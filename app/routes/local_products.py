from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

# 📁 Ruta absoluta a la carpeta /data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)


@router.get("/search")
async def search_local_products(
    query: str = Query(..., description="Texto a buscar (por nombre, marca, color, talle, etc.)"),
    page: int = Query(1, description="Número de página"),
    per_page: int = Query(50, description="Cantidad de resultados por página (default 50)")
):
    """
    Endpoint de búsqueda local optimizado.
    Lee los archivos JSON por lotes sin mantener todo en memoria.
    Devuelve coincidencias paginadas y listas para consumir por Lyzr.
    """
    keywords = [q.strip().lower() for q in query.split() if q.strip()]
    matched = []
    seen_ids = set()

    # 🔹 Leer archivos JSON uno por uno (evita sobrecargar la memoria)
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Si el archivo está anidado (texto JSON dentro de JSON)
                if isinstance(data, str):
                    data = json.loads(data)

                # Convertir a lista si es un solo producto
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    print(f"⚠️ Archivo {filename} no contiene una lista válida. Se omite.")
                    continue

                # 🔍 Buscar coincidencias en el archivo actual
                for p in data:
                    if not isinstance(p, dict):
                        continue

                    # Evitar duplicados
                    pid = p.get("ID")
                    if pid in seen_ids:
                        continue
                    seen_ids.add(pid)

                    # Texto completo para búsqueda flexible
                    text = " ".join([
                        str(p.get("Nombre", "")),
                        str(p.get("Marca", "")),
                        str(p.get("Categoría", "")),
                        str(p.get("Color", "")),
                        str(p.get("Talle", "")),
                    ]).lower()

                    if all(k in text for k in keywords):
                        matched.append({
                            "ID": p.get("ID"),
                            "Nombre": p.get("Nombre"),
                            "Marca": p.get("Marca"),
                            "Categoría": p.get("Categoría"),
                            "Color": p.get("Color"),
                            "Talle": p.get("Talle"),
                            "Precio": p.get("Precio"),
                            "Stock": p.get("Stock"),
                            "URL": p.get("URL"),
                            "Imagen": p.get("Imagen")
                        })

        except Exception as e:
            print(f"❌ Error al procesar {filename}: {e}")

    # 🔹 Paginación segura
    total = len(matched)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = matched[start:end]

    # 🔹 Respuesta final optimizada para Lyzr
    return {
        "query": query,
        "page": page,
        "results_count": len(paginated),
        "total_found": total,
        "has_more": total > end,
        "products": paginated,
    }
