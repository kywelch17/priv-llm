import numpy as np

from app.clients import ai

def search(cn, question: str, k: int = 3):
    qvec = np.array(ai.embed([question])[0])
    return cn.execute(
        "SELECT c.content, d.filename, c.embedding <=> %s AS dist "
        "FROM chunks c JOIN documents d ON d.id = c.document_id "
        "ORDER BY dist LIMIT %s",
        (qvec, k),
    ).fetchall()