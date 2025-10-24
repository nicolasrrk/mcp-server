from dotenv import load_dotenv
load_dotenv()  # Carga las variables del archivo .env antes que todo lo demás

from fastapi import FastAPI
from app.routes import lyzr_tools, health, webhook, tiendanube, local_products

app = FastAPI(title="MCP Server - LucidBot Connector")

# Rutas
app.include_router(health.router)
app.include_router(lyzr_tools.router, prefix="/lyzr")
app.include_router(webhook.router, prefix="/webhook")
app.include_router(tiendanube.router, prefix="/tiendanube")
app.include_router(local_products.router, prefix="/local-products")


@app.get("/")
def root():
    return {"status": "MCP Server está corriendo"}

