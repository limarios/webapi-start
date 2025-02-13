from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    data_inicio = Column(DateTime, default=datetime.now)
    data_fim = Column(DateTime, nullable=True)
    tipo = Column(String(100), nullable=True)
    titulo = Column(String(100), nullable=True)
    descricao = Column(Text, nullable=True)
    status = Column(String(20), nullable=True)

    # Relacionamento com ActivityError
    erros = relationship('ActivityError', back_populates='atividade', lazy=True)

    # Relacionamentos com Customer e User
    cliente = relationship('Customer', back_populates='activities')
    usuario = relationship('User', back_populates='activities')

    def __repr__(self):
        return f'<Activity {self.titulo}>'
