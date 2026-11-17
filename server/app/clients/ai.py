from ollama import Client
from app.config import settings

client = Client(host=settings.ollama_url)

def chat(prompt: str) -> str:
    resp = client.chat(
        model=settings.chat_model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )

    return resp.message.content

def embed(texts: list[str]) -> list[list[float]]:
    resp = client.embed(
        model=settings.embed_model,
        input=texts
    )

    return resp.embeddings
