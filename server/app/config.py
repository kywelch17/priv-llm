from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    database_url: str
    ollama_url: str = "http://ubuntu-vm:11434"
    chat_model: str = "llama3.2"
    embed_model: str = "nomic-embed-text"
    upload_dir: Path = Path("uploads")

settings = Settings()
