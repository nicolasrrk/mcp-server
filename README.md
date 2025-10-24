# 🧠 MCP Server – Lyzr Connector  
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?logo=render&logoColor=white)
![Status](https://img.shields.io/badge/Status-Online-success)
![License](https://img.shields.io/badge/License-MIT-blue)

Servidor **MCP (Modular Command Protocol)** desarrollado en **Python + FastAPI**, diseñado para conectar **Lyzr**, **LucidBot** y APIs externas como **Tienda Nube**, procesando datos en lotes y ofreciendo una integración escalable y eficiente.

---

## 🚀 Características principales

- 🔗 **Integración completa con Lyzr y LucidBot**
- ⚙️ **Estructura modular en FastAPI** (rutas limpias y organizadas)
- 📦 **Procesamiento eficiente de productos CSV por lotes**
- 🔍 **Búsqueda rápida de productos desde archivo CSV**
- ☁️ **Despliegue automático en Render**
- 🧰 **Integrable con herramientas externas o agentes inteligentes**

---

## 🗂️ Estructura del proyecto

mcp-server/
│
├── app/
│ ├── main.py # Punto de entrada principal
│ │
│ ├── routes/ # Rutas del servidor
│ │ ├── health.py
│ │ ├── lyzr_tools.py
│ │ ├── tiendanube.py # Lógica de búsqueda de productos CSV por lotes
│ │ └── webhook.py
│ │
│ ├── utils/ # Funciones auxiliares y scripts
│ │ ├── split_products_csv.py # Divide el CSV original en lotes JSON
│ │ └── lyzr_client.py # Comunicación con la API de Lyzr
│ │
│ └── data/ # Archivos CSV divididos
│ ├── products_batch_1.csv
│ ├── products_batch_2.csv
│ └── metadata.json
│
├── .env # Variables de entorno
├── requirements.txt # Dependencias del proyecto
├── Procfile # Configuración de Render
└── README.md


---

## ⚙️ Instalación local

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/nicolasrrk/mcp-server.git
cd mcp-server
2️⃣ Crear y activar entorno virtual
bash
Copiar código
python -m venv venv
venv\Scripts\activate      # En Windows
# o
source venv/bin/activate   # En Linux/Mac
3️⃣ Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
4️⃣ Configurar variables de entorno
Crea un archivo .env en la raíz con tus credenciales:

ini
Copiar código
LYZR_API_KEY=<tu_api_key_lyzr>
TIENDANUBE_TOKEN=<tu_token_tiendanube>
5️⃣ Ejecutar el servidor localmente
bash
Copiar código
uvicorn app.main:app --reload
El servidor quedará disponible en:

arduino
Copiar código
http://localhost:8000
🔍 Endpoint de búsqueda de productos (por lotes CSV)
Ruta: /tiendanube/search
Método: POST

Ejemplo de uso
bash
Copiar código
curl -X POST http://localhost:8000/tiendanube/search \
-H "Content-Type: application/json" \
-d "{\"query\": \"chatita\", \"page\": 1}"
Ejemplo de respuesta
json
Copiar código
{
  "query": "chatita",
  "page": 1,
  "results_count": 3,
  "has_more": false,
  "products": [
    {
      "id": 271417912,
      "name": "Chatita Modare 016461",
      "brand": "Modare",
      "category": "Dama",
      "color": "Negro",
      "price": "$32.490",
      "url": "https://mayorista.pampashop.com.ar/productos/Chatita-Mujer-Modare-016461/",
      "image": "https://acdn-us.mitiendanube.com/stores/006/139/677/products/821016461sneg.png"
    }
  ]
}
🧩 Integración con Lyzr
Para registrar la herramienta en tu agente Lyzr:

json
Copiar código
{
  "name": "search_products",
  "description": "Busca productos del catálogo de Tienda Nube por nombre, color o categoría.",
  "type": "api",
  "url": "https://<tu-servidor>.onrender.com/tiendanube/search",
  "method": "POST",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Texto de búsqueda del producto" },
      "page": { "type": "integer", "description": "Número de página (opcional)" }
    },
    "required": ["query"]
  }
}
El agente podrá buscar productos como:

nginx
Copiar código
buscar "zapatilla blanca talle 36"
📦 Dependencias principales
txt
Copiar código
# === Servidor FastAPI ===
fastapi>=0.115.0
uvicorn>=0.30.0

# === HTTP requests ===
httpx>=0.27.0

# === Variables de entorno ===
python-dotenv>=1.0.1

# === Caché ===
cachetools>=5.3.3

# === Tipado y validación ===
pydantic>=2.8.2

# === Manipulación de CSV / JSON ===
pandas>=2.2.2

# === Testing ===
pytest>=8.3.2
☁️ Despliegue en Render
Subí tus cambios a GitHub.

Iniciá sesión en Render.

Crea un nuevo Web Service desde tu repositorio.

En “Start Command” colocá:

nginx
Copiar código
uvicorn app.main:app --host 0.0.0.0 --port 10000
Agregá tus variables de entorno (desde el panel de Render).

Deploy 🚀

👨‍💻 Autor
Pablo Nicolás Ramírez
🧠 Desarrollador e Integrador MCP + Lyzr
Integración completa con LucidBot, Tienda Nube y Render

📧 nicolasrrk.dev@gmail.com
🌐 github.com/nicolasrrk

