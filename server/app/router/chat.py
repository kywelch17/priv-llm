from fastapi import APIRouter, HTTPException
from ollama import ResponseError

from app.db import get_cn
from app.clients import ai
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services import retrieval, prompts

router = APIRouter(prefix="/chat", tags=["chat", "ai", "llama"])

@router.post("/query", response_model=ChatResponse)
def query(body: ChatRequest):
    with get_cn() as cn:
        rows = retrieval.search(cn, body.query, body.k)

    if not rows:
        return ChatResponse(
            answer="No doc uploaded yet!",
            sources=[]
        )

    try:
        answer = ai.chat(prompt=prompts.build_prompt(body.query, rows))
    except ResponseError as e:
        raise HTTPException(502, f"Ollama error: {e}")

    return ChatResponse(
        answer=answer,
        sources=[
            Source(n=i + 1, filename=r[1], snippet=r[0][:200], distance=float(r[2]))
            for i, r in enumerate(rows)
        ]
    )