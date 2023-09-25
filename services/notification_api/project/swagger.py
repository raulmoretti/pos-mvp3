from flask_restx import Api, Namespace, fields

# Inicializando a API
api = Api(
    version='1.0', 
    title='API de Notificações', 
    description='API para gerenciamento de notificações', 
    doc='/swagger'
)

# Declaração do namespace para a API
api_v1 = Namespace('notification_api', 
                   description='Serviço de armazenamento de notificações e webhook para atualização de distância e tempo estimado de entregas.')

# Declaração do modelo para a API
model = api_v1.model('Notificacoes', {
    'id': fields.Integer(readonly=True),
    'entrega_id': fields.Integer(description="ID da Entrega"),
    'email': fields.String(required=True, description="Email do Cliente"),
    'destinatario': fields.String(required=True, description="Nome do Destinatário"),
    'status': fields.String(required=True, description="Status da Entrega"),
    'cidade_atual': fields.String(required=True, description="Cidade Atual onde a Entrega se encontra"),
    'cidade_destino': fields.String(required=True, description="Cidade Destino da Entrega"),
    'tempo_estimado': fields.String(description="Tempo Estimado calculado com base na cidade atual e na cidade de destino pela Google Matrix API. Não pode ser editado manualmente."),
    'distancia_atual': fields.Float(description="Distância Atual (em metros) calculada com base na cidade atual e na cidade de destino pela Google Matrix API. Não pode ser editado manualmente."),
    'created_at': fields.DateTime(readonly=True, description="Data de Criação da Notificação")
})