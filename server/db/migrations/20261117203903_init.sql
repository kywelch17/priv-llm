-- migrate:up
CREATE TABLE IF NOT EXISTS documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    filename text NOT NULL,
    file_type text NOT NULL,
    status text NOT NULL DEFAULT 'processing',
    error text,
    storage_path text,
    size_bytes bigint,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chunks (
    id bigserial PRIMARY KEY,
    document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index int NOT NULL,
    content text NOT NULL,
    embedding vector(768),
    page int,
    start_sec real,
    end_sec real
);

CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY default gen_random_uuid(),
    first_name text NOT NULL,
    surname text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    created_at timestamptz NOT NULL default now(),
    updated_at timestamptz NOT NULL default now()
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- migrate:down
DROP TABLE IF EXISTS chunks;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS users;