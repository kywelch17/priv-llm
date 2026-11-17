import httpx
import psycopg as pc
from fastapi import FastAPI
from config import settings

app = FastAPI()

@app.get("/health")
def health():
    result = {}

    try:
        with pc.connect(settings.database_url) as cn:
            cn.execute("SELECT 1")
            result["postgres"] = "ok"
    except Exception as e:
        result["postgres"] = f"error: {e}"

    try:
        resp = httpx.get(f"{settings.ollama_url}/api/tags", timeout=5)
        result["ai"] = [m["name"] for m in resp.json()["models"]]
    except Exception as e:
        result["ai"] = f"error: {e}"

    return result
