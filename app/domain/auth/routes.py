from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.auth import verify_password
from app.domain.user.service import UserService
from app.domain.user.repository import UserRepository
from app.db.session import get_db

router = APIRouter()

# 🔥 Correção: Configurar corretamente o tokenUrl
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def authenticate_user(username: str, password: str, service: UserService):
    user = await service.get_user_by_username(username)  # Adicione await aqui
    if not user:
        return None
    if not verify_password(password, user.senha):  # user.senha agora está acessível corretamente
        return None
    return user


@router.post("/token", summary="Obter Token de Acesso", tags=["Autenticação"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    service = UserService(UserRepository(db))
    user = await authenticate_user(form_data.username, form_data.password, service)  # Adicione await aqui
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", summary="Obter usuário autenticado", tags=["Autenticação"])
def read_users_me(token: str = Security(oauth2_scheme)):
    return {"token_recebido": token}
