from dotenv import load_dotenv
load_dotenv()  # Carga las variables del archivo .env antes que todo lo demás

from fastapi import FastAPI
from app.routes import lyzr_tools, health, webhook, tiendanube

app = FastAPI(title="MCP Server - LucidBot Connector")

# Rutas
app.include_router(health.router)
app.include_router(lyzr_tools.router, prefix="/lyzr")
app.include_router(webhook.router, prefix="/webhook")
app.include_router(tiendanube.router, prefix="/tiendanube")

@app.get("/")
def root():
    return {"status": "MCP Server está corriendo"}

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

