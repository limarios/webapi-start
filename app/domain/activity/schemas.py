from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ActivityBase(BaseModel):
    cliente_id: int
    usuario_id: int
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None


class ActivityCreate(ActivityBase):
    cliente_id: int
    usuario_id: int
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None


class ActivityRead(ActivityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivityUpdate(BaseModel):
    cliente_id: Optional[int] = None
    usuario_id: Optional[int] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
