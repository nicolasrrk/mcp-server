import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LYZR_API_KEY")
BASE_URL = os.getenv("LYZR_BASE_URL")

async def query_lyzr(message: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    body = {"input": [{"role": "user", "content": message}]}
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, json=body, headers=headers)
        return response.json()
