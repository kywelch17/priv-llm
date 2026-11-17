SYSTEM_PROMPT = (
    "Answer using only the context below. If the answer isn't there, "
    "say you don't know. Cite sources like [1] [2] and so on."
)

def build_prompt(query, rows): 
    context = "\n\n".join(f"[{i+1}] ({r[1]})\n{r[0]}" for i, r in enumerate(rows))
    return f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuery: {query}"

