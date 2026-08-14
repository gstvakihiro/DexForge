"""
Configuração da conexão com o banco de dados via SQLAlchemy.

- `engine`: a conexão em si com o PostgreSQL.
- `SessionLocal`: fábrica de sessões (cada requisição usa uma sessão própria).
- `Base`: classe que todos os modelos (tabelas) vão herdar.
- `get_db`: função usada pelo FastAPI para injetar uma sessão de banco
  em cada endpoint que precisar, e garantir que ela é fechada no final.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
