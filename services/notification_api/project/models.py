from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from project import db

Base = declarative_base()

class Notificacao(db.Model):
    __tablename__ = "notificacoes"

    id = db.Column(db.Integer, primary_key=True)
    
    entrega_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    destinatario = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(200), nullable=False)  
    cidade_atual = db.Column(db.String(100), nullable=False)
    cidade_destino = db.Column(db.String(100), nullable=False)

    tempo_estimado = db.Column(db.String(100))
    distancia_atual = db.Column(db.Float)

    created_at = Column(DateTime, default=func.now())
            
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs}