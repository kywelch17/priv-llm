from hashlib import sha256
from fastapi import APIRouter, HTTPException, UploadFile
from pathlib import Path

from app.db import get_cn
from app.config import settings
from app.services import chunker
from app.clients import ai
# from app.clients.ollama import embed

router = APIRouter(prefix="/docs", tags=["documents"])

@router.post("")
async def upload(file: UploadFile):
    if not file.filename.endswith(".txt"):
        raise HTTPException(400, "Only txt files for now!")

    doc_id = ""
    data = await file.read()
    sha = sha256(data).hexdigest()
    path = Path(settings.upload_dir) / f"{sha}.txt"
    if path.exists():
        raise HTTPException(409, {
            "file": file.filename,
            "msg": "File already exists"
        })

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

    try:
        text = data.decode()
        with get_cn() as cn:
            doc_id = cn.execute(
                "INSERT INTO documents (filename, file_type, storage_path, size_bytes)" \
                "VALUES (%s, %s, %s, %s) RETURNING id;",
                (file.filename, ".txt", str(path), len(data))
            ).fetchone()[0]
            # return {"id": str(doc_id), "characters": text}
            pieces = chunker.chunk_text(text)
            vector = ai.embed(pieces)
            with cn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO chunks (document_id, chunk_index, content, embedding)" \
                    "VALUES (%s, %s, %s, %s);",
                    [(doc_id, i, c, v) for i, (c, v) in enumerate(zip(pieces, vector))] 
                )
            cn.execute("UPDATE documents SET status = 'ready' WHERE id = %s;", (doc_id,))
            return {
                "id": str(doc_id), 
                "characters": text,
                "pieces": pieces
            }
    except UnicodeDecodeError:
        raise HTTPException(400, "File isn't valid UTF-8 text") 
    except OSError as e:
        raise HTTPException(502, f"error: {e}")
    



@router.get("")
def list_docs():
    with get_cn() as cn:
        rows = cn.execute(
            "SELECT filename, file_type, status, created_at FROM documents ORDER BY created_at DESC;"
        ).fetchall()

        return [{
            "filename": r[0],
            "filetype": r[1],
            "status": r[2],
            "createdAt": r[3]
        } for r in rows]
