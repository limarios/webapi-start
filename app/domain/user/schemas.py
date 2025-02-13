from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Base para compartilhamento de atributos (entrada/saída)
class UserBase(BaseModel):
    nome: str
    email: EmailStr
    login: str
    grupo: str
    telefone: str
    cargo: Optional[str] = None
    setor: Optional[str] = None
    ativo: Optional[str] = None

# Schema para criar um novo usuário
class UserCreate(UserBase):
    senha: str  # Campo necessário para criação

# Schema para ler/retornar dados do usuário (ex.: GET)
class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Schema para atualizar um usuário parcialmente (opcional)
class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    login: Optional[str] = None
    grupo: Optional[str] = None
    telefone: Optional[str] = None
    cargo: Optional[str] = None
    setor: Optional[str] = None
    ativo: Optional[str] = None
