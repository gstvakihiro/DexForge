"""
Ponto de entrada da aplicação FastAPI.

Roda com:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.routers import auth

app = FastAPI(
    title="DexForge API",
    description="Backend da DexForge — uma Pokédex completa.",
    version="0.1.0",
)

app.include_router(auth.router)

# Libera o frontend (rodando em outra porta) a fazer requisições pra essa API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint simples pra confirmar que a API está no ar
    E que a conexão com o banco de dados está funcionando.
    """
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "environment": settings.environment,
        "database": "connected",
    }


@app.get("/")
def root():
    return {"message": "DexForge API está rodando. Veja /docs para a documentação."}
