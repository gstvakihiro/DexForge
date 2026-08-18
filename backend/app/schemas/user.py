"""
Schemas Pydantic: definem o formato dos dados que entram e saem da API.

Diferente do modelo em app/models/user.py (que representa a tabela no banco),
esses schemas representam o "contrato" da API — o que o frontend recebe.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    """Formato do usuário devolvido pela API (nunca inclui dados sensíveis)."""

    id: uuid.UUID
    email: str
    nome: str
    avatar_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Formato da resposta do login: os dois tokens + dados básicos do usuário."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut
