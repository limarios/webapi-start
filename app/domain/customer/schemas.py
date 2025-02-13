from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import Optional

class CustomerBase(BaseModel):
    razao_social: str = Field(..., example="Empresa Exemplo S/A")
    nome_fantasia: str = Field(..., example="Exemplo")
    cpfecnpj: Optional[str] = Field(None, example="12.345.678/0001-99")
    cpf: Optional[str] = Field(None, example="123.456.789-00")
    inscricao_estadual: Optional[str] = Field(None, example="123456789")
    inscricao_municipal: Optional[str] = Field(None, example="987654321")
    telefone: Optional[str] = Field(None, example="(11) 1234-5678")
    celular: Optional[str] = Field(None, example="(11) 91234-5678")
    email: Optional[EmailStr] = Field(None, example="contato@exemplo.com")
    regime_tributario: Optional[str] = Field(None, example="Simples Nacional")
    tipo_conta: Optional[str] = Field(None, example="Corrente")
    endereco: Optional[str] = Field(None, example="Rua Exemplo")
    bairro: Optional[str] = Field(None, example="Centro")
    cidade: Optional[str] = Field(None, example="São Paulo")
    estado: Optional[str] = Field(None, example="SP")
    numero: Optional[str] = Field(None, example="123")
    cep: Optional[str] = Field(None, example="01234-567")
    complemento: Optional[str] = Field(None, example="Sala 1")
    login_gov: Optional[str] = Field(None, example="usuario_gov")
    senha_gov: Optional[str] = Field(None, example="senha123")
    certificado: Optional[bool] = Field(False, example=True)
    zap_contabil: Optional[bool] = Field(False, example=True)
    representante: Optional[str] = Field(None, example="João da Silva")
    email1_iss: Optional[str] = Field(None, example="email1@exemplo.com")
    email2_iss: Optional[str] = Field(None, example="email2@exemplo.com")
    email3_iss: Optional[str] = Field(None, example="email3@exemplo.com")

    model_config = ConfigDict(from_attributes=True)

    # Converte strings vazias para None para o campo email
    @validator('email', pre=True, always=True)
    def empty_string_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

class CustomerCreate(CustomerBase):
    pass  # Adicione campos obrigatórios para criação, se necessário

class CustomerRead(CustomerBase):
    id: int

class CustomerUpdate(BaseModel):
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cpfecnpj: Optional[str] = None
    cpf: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[EmailStr] = None
    regime_tributario: Optional[str] = None
    tipo_conta: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    numero: Optional[str] = None
    cep: Optional[str] = None
    complemento: Optional[str] = None
    login_gov: Optional[str] = None
    senha_gov: Optional[str] = None
    certificado: Optional[bool] = None
    zap_contabil: Optional[bool] = None
    representante: Optional[str] = None
    email1_iss: Optional[str] = None
    email2_iss: Optional[str] = None
    email3_iss: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
