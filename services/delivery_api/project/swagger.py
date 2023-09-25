from flask_restx import Api, Namespace, fields

# Inicializando a API
api = Api(
    version='1.0', 
    title='API de Entregas', 
    description='Uma API simples de Entregas', 
    doc='/swagger'
)

# Declaração do namespace para a API
api_v1 = Namespace('delivery_api', 
                   description='API de Entregas. Rotas para buscar, criar, atualizar e deletar entregas.')

# Declaração do modelo para a API
model = api_v1.model('Entrega', {
    'id': fields.Integer(readonly=True),
    'remetente': fields.String(required=True, description='Pessoa que envia a entrega'),
    'destinatario': fields.String(required=True, description='Pessoa que recebe a entrega'),
    'endereco_origem': fields.String(required=True, description='Endereço completo de origem'),
    'endereco_destino': fields.String(required=True, description='Endereço completo de destino'),
    'descricao': fields.String(required=True, description='Descrição do(s) pacote(s)'),
    'peso': fields.Float(required=True, description='Peso total da entrega'),
    'cidade_origem': fields.String(required=True, description='Cidade de origem'),
    'cidade_destino': fields.String(required=True, description='Cidade de destino. Campo utilizado para calcular a distância e o tempo estimado'),
    'status': fields.String(description='Status da entrega. Default: Aguardando coleta'),
    'cidade_atual': fields.String(required=True, description='Cidade atual onde a entrega se encontra. Campo utilizado para calcular a distância e o tempo estimado'),
    'tempo_estimado': fields.String(description='Tempo estimado para a entrega. Calculo feito automaticamente com base na cidade atual e na cidade de destino, e não pode ser editado manualmente'),
    'distancia_atual': fields.Float(description='Distância atual (em metros) para a entrega. Calculo feito automaticamente com base na cidade atual e na cidade de destino, e não pode ser editado manualmente')
})