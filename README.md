# MCP Server – LucidBot Connector

Servidor MCP (Modular Command Protocol) desarrollado en **Python + FastAPI**  
para conectar **LucidBot** y **LyZR**, gestionando consultas, herramientas y APIs externas
(por ejemplo, Tienda Nube).

---

## Características

- Servidor modular con rutas organizadas
- Comunicación directa con **LyZR API**
- Preparado para integrarse con **LucidBot** o **n8n**
- Desplegable fácilmente en **Render** o cualquier servicio cloud

---

## Estructura del proyecto
mcp-server/
│
├── app/
│ ├── main.py
│ ├── routes/
│ │ ├── health.py
│ │ ├── lyzr_tools.py
│ │ └── webhook.py
│ └── utils/
│ └── lyzr_client.py
│
├── .env
├── requirements.txt
├── Procfile
└── README.md

---

## ⚙️ Instalación local

```bash
git clone https://github.com/<tu_usuario>/mcp-server.git
cd mcp-server
python -m venv venv
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
