from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
import os

# Definir o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Definir qual arquivo .env carregar (padrão: .env)
env_file = BASE_DIR / ".env"

# Verificar se estamos em produção e mudar para outro arquivo, se necessário
if os.getenv("ENV") == "production":
    env_file = BASE_DIR / ".env.production"
elif os.getenv("ENV") == "development":
    env_file = BASE_DIR / ".env.development"
elif os.getenv("ENV") == "testing":
    env_file = BASE_DIR / ".env.testing"

# Carregar as variáveis do .env correto
load_dotenv(env_file)
print(f"🔍 Carregando arquivo .env: {env_file}")

class Settings(BaseSettings):
    """Configurações da API usando Pydantic para validação"""

    # Banco de dados
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASS: str = os.getenv("DB_PASS", "rootpassword")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "automation_alcance")

    # Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Configuração de Debug e Ambiente
    DEBUG: bool = os.getenv("DEBUG", "False").strip().lower() in ["true", "1"]
    ENV: str = os.getenv("ENV", "development")  # Pode ser "development", "production", "testing"

    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    """Cria um cache das configurações para evitar recarregamento desnecessário"""
    return Settings()

# Instância global das configurações
settings = get_settings()
