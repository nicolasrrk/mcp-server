import os
import json
import math
import pandas as pd
from datetime import datetime

# 📂 Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/utils
CSV_PATH = os.path.join(BASE_DIR, "productos.csv")     # archivo dentro de /utils
DATA_DIR = os.path.join(BASE_DIR, "..", "data")        # guarda los JSON en /app/data
CHUNK_SIZE = 500                                       # cantidad de productos por lote


def split_csv_into_json():
    # Crear carpeta destino si no existe
    os.makedirs(DATA_DIR, exist_ok=True)

    # Verificar existencia del archivo CSV
    if not os.path.exists(CSV_PATH):
        print(f"❌ No se encontró el archivo CSV en: {CSV_PATH}")
        return

    # Leer CSV con pandas
    df = pd.read_csv(CSV_PATH)

    total = len(df)
    chunks = math.ceil(total / CHUNK_SIZE)

    print(f"📦 Total de productos: {total}")
    print(f"✂️ Dividiendo en {chunks} archivos JSON...")

    # Guardar cada fragmento
    for i in range(chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk = df.iloc[start:end]

        path = os.path.join(DATA_DIR, f"products_{i+1}.json")
        chunk.to_json(path, orient="records", force_ascii=False, indent=2)

        print(f"✅ Guardado: {path} ({len(chunk)} productos)")

    # Guardar metadatos del proceso
    metadata = {
        "total_products": total,
        "chunks": chunks,
        "updated_at": datetime.now().isoformat()
    }

    with open(os.path.join(DATA_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("🧩 División completa.")


if __name__ == "__main__":
    split_csv_into_json()
