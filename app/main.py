from fastapi import FastAPI
from app.routes import lyzr_tools, health, webhook

app = FastAPI(title="MCP Server - LucidBot Connector")

app.include_router(health.router)
app.include_router(lyzr_tools.router, prefix="/lyzr")
app.include_router(webhook.router, prefix="/webhook")

@app.get("/")
def root():
    return {"status": "MCP Server esta corriendp"}
