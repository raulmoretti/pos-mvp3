from project import db

class Entrega(db.Model):
    __tablename__ = "entregas"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(50), nullable=False)
    remetente = db.Column(db.String(50), nullable=False)
    destinatario = db.Column(db.String(50), nullable=False)
    endereco_origem = db.Column(db.String(100), nullable=False)
    endereco_destino = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    cidade_origem = db.Column(db.String(100), nullable=False)
    cidade_destino = db.Column(db.String(100), nullable=False)
    cidade_atual = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(200), default='Aguardando coleta')

    tempo_estimado = db.Column(db.String(100))
    distancia_atual = db.Column(db.Float)

            
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in db.inspect(self).mapper.column_attrs}