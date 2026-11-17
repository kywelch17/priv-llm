from pydantic import BaseModel, Field

class Source(BaseModel):
    n: int
    filename: str
    snippet: str
    distance: float

class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2400)
    k: int = Field(default=3, ge=1, le=5)

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
