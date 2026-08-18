"""
Endpoints de autenticação via Google OAuth.

Fluxo completo:
1. Frontend chama GET /auth/google/login
2. Esse endpoint redireciona o usuário pro Google
3. Usuário confirma login/permissões no Google
4. Google redireciona de volta pra GET /auth/google/callback com um "code"
5. Trocamos esse "code" por um access_token do Google
6. Usamos esse access_token pra pegar email/nome/foto do usuário
7. Criamos ou atualizamos o usuário no nosso banco
8. Geramos nosso próprio JWT e devolvemos pro frontend
"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

bearer_scheme = HTTPBearer()


@router.get("/google/login")
def google_login():
    """
    Monta a URL de login do Google e redireciona o usuário pra lá.
    O frontend só precisa direcionar o navegador pra essa rota.
    """
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{query}")


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Recebe o "code" do Google, troca por dados do usuário,
    cria/atualiza no banco e devolve nossos próprios tokens.
    """
    # 1. Troca o "code" por um access_token do Google
    token_response = httpx.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.google_redirect_uri,
        },
    )
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Falha ao trocar code por token com o Google")

    google_access_token = token_response.json()["access_token"]

    # 2. Usa esse token pra pegar os dados do usuário
    userinfo_response = httpx.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {google_access_token}"},
    )
    if userinfo_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Falha ao buscar dados do usuário no Google")

    google_user = userinfo_response.json()
    # google_user contém: sub (id único), email, name, picture

    # 3. Cria ou atualiza o usuário no nosso banco
    user = db.query(User).filter(User.provider_id == google_user["sub"]).first()

    if user is None:
        user = User(
            email=google_user["email"],
            nome=google_user["name"],
            avatar_url=google_user.get("picture"),
            provider="google",
            provider_id=google_user["sub"],
        )
        db.add(user)
    else:
        user.nome = google_user["name"]
        user.avatar_url = google_user.get("picture")

    db.commit()
    db.refresh(user)

    # 4. Gera nossos próprios tokens
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    # 5. Redireciona de volta pro frontend, com os tokens na URL
    #    (Numa fase futura, o refresh_token deve ir num cookie httpOnly em vez de URL,
    #     por segurança. Por ora, versão simples pra validar o fluxo ponta a ponta.)
    redirect_url = (
        f"{settings.frontend_url}/auth/callback"
        f"?access_token={access_token}&refresh_token={refresh_token}"
    )
    return RedirectResponse(redirect_url)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency usada em qualquer endpoint que exige usuário autenticado.
    Lê o token do header "Authorization: Bearer <token>", valida, e busca o usuário.
    """
    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    return user


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Endpoint de teste: devolve os dados do usuário logado, a partir do token."""
    return current_user
