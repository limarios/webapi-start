from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base  # Supondo que você tenha esse arquivo de base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nome = Column(String(300), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    login = Column(String(100), nullable=False)
    grupo = Column(String(30), nullable=False)
    telefone = Column(String(30), nullable=False)
    cargo = Column(String(50))
    setor = Column(String(50))
    ativo = Column(String(20))

    # Relacionamento com Activity
    activities = relationship('Activity', back_populates='usuario', lazy=True)

    
    def __repr__(self):
        return f'<User {self.nome}>'
