"""
Modelo da tabela de usuários.

Cada linha aqui vira uma coluna na tabela `users` do PostgreSQL.
"""

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Dados vindos do Google (ou de cadastro futuro por email/senha)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # De onde veio esse usuário: "google" por enquanto, "local" no futuro
    provider: Mapped[str] = mapped_column(
        String(50), default="google", nullable=False)

    # ID único que o Google usa pra identificar essa conta (evita duplicar usuário)
    provider_id: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
