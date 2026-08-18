"""
Funções relacionadas a segurança: criação e validação de tokens JWT.

Fluxo:
- create_access_token: gera um token de curta duração (usado nas requisições normais)
- create_refresh_token: gera um token de longa duração (usado só pra renovar o access token)
- decode_token: valida um token recebido e devolve os dados de dentro dele
"""

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from app.core.config import settings


def _create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "access"},
        timedelta(minutes=settings.jwt_access_token_expire_minutes),
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "type": "refresh"},
        timedelta(days=settings.jwt_refresh_token_expire_days),
    )


def decode_token(token: str) -> dict | None:
    """Valida o token e devolve os dados dentro dele, ou None se for inválido/expirado."""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None
