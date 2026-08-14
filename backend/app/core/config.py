"""
Configurações centrais da aplicação.

Este arquivo lê as variáveis do arquivo .env automaticamente
(usando pydantic-settings) e disponibiliza elas de forma
tipada e organizada pro resto do código.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Banco de dados
    database_url: str

    # Redis (cache) — vamos usar de verdade a partir da Fase 2
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # OAuth Google
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    # Geral
    environment: str = "development"
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instância única, reutilizada em todo o projeto
settings = Settings()
