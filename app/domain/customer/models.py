from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    razao_social = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200), nullable=False)
    cpfecnpj = Column(String(255))
    cpf = Column(String(30))
    inscricao_estadual = Column(String(50))
    inscricao_municipal = Column(String(50))
    telefone = Column(String(50))
    celular = Column(String(50))
    email = Column(String(100))
    regime_tributario = Column(String(100))
    tipo_conta = Column(String(20))
    endereco = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(5))
    numero = Column(String(10))
    cep = Column(String(10))
    complemento = Column(String(100))
    login_gov = Column(String(250))
    senha_gov = Column(String(250))
    certificado = Column(Boolean, default=False)
    zap_contabil = Column(Boolean, default=False)
    representante = Column(String(50))

    # Alíquota ISS:
    email1_iss = Column(String(300))
    email2_iss = Column(String(300))
    email3_iss = Column(String(300))

    activities = relationship('Activity', back_populates='cliente', lazy=True)


    def __repr__(self):
        return f'<Customer {self.razao_social}>'
