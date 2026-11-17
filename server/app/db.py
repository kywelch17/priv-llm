from contextlib import contextmanager
from psycopg_pool import ConnectionPool
from pgvector.psycopg import register_vector
from app.config import settings

def _configure(cn):
    register_vector(cn)

pool = ConnectionPool(
    settings.database_url,
    min_size=1,
    max_size=10,
    configure=_configure,
    open=False,
)

@contextmanager
def get_cn():
    with pool.connection() as conn:
        yield conn