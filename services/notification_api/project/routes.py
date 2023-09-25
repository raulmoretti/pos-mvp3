import os
from flask import request
from project.models import Notificacao
from project import db
from .google_api import google_matrix_api_request
from project.swagger import api_v1, model
from flask_restx import Resource
from project.mailjet_api import mailjet


@api_v1.route('/notificacao/<int:id>')
class NotificacoesResource(Resource):
    @api_v1.marshal_with(model)
    def get(self, id):
        """
        Buscar a notificação de uma entrega específica pelo ID da entrega, se existir, e mandar uma notificação por email utilizando a API do Mailjet.
        """
        try:
            notificacao = Notificacao.query.filter_by(entrega_id=id).first()
            if notificacao:
                data = {
                    'Messages': [
                        {
                        "From": {
                            "Email": os.getenv('MAILJET_SENDER_EMAIL'),
                            "Name": os.getenv('MAILJET_SENDER_NAME')
                        },
                        "To": [
                            {
                            "Email": notificacao.email,
                            "Name": notificacao.destinatario
                            }
                        ],
                        "Subject": "Notificação de entrega",
                        "TextPart": "Notificação de entrega",
                        "HTMLPart": f"<h3>Notificação de entrega</h3><br />Entrega ID: {notificacao.entrega_id}<br />Status: {notificacao.status}<br />Cidade atual: {notificacao.cidade_atual}<br />Cidade destino: {notificacao.cidade_destino}<br />Distância atual: {notificacao.distancia_atual}<br />Tempo estimado: {notificacao.tempo_estimado}",
                        "CustomID": "AppGettingStartedTest"
                        }
                    ]
                }
                # Manda notificação por email usando a API do Mailjet
                mailjet.send.create(data=data)

            return notificacao, 200
        except Exception as e:
            return {'message': 'Erro ao buscar notificação', 'error': str(e)}

    def delete(self, id):
        """
        Deletar uma notificação específica pelo ID da entrega
        """
        try:
            notificacao = Notificacao.query.filter_by(entrega_id=id).first()
            if notificacao:
                db.session.delete(notificacao)
                db.session.commit()
                return {'message': 'Notificação deletada com sucesso'}, 200
            else:
                return {'message': 'Notificação não encontrada'}, 404
        except Exception as e:
            return {'message': 'Erro ao deletar notificação', 'error': str(e)}

@api_v1.route('/webhook')
class WebhookResource(Resource):
    @api_v1.expect(model)
    @api_v1.marshal_with(model)
    def post(self):
        """
        Atualizar uma notificação específica pelo ID da entrega.
        Campos obrigatórios: entrega_id, email, destinatario, status, cidade_atual, cidade_destino

        Campos opcionais: nenhum

        Campos não editáveis: distancia_atual, tempo_estimado

        Pela cidade_atual e cidade_destino, este webhook faz uma requisição para a API do Google Maps para obter a distância_atual e o tempo_estimado.
        """
        try: 
            data = request.get_json()
            google_data = google_matrix_api_request(data['cidade_atual'], data['cidade_destino'])
            notificacao = Notificacao.query.filter_by(entrega_id=data['entrega_id']).first()

            # Se a notificação não existir, criamos uma nova.
            if not notificacao:
                notificacao = Notificacao(
                    entrega_id=data['entrega_id'], 
                    status=data['status'], 
                    cidade_atual=data['cidade_atual'], 
                    cidade_destino=data['cidade_destino'],
                    email=data['email'],
                    destinatario=data['destinatario']
                )
                db.session.add(notificacao)

            notificacao.distancia_atual = google_data['rows'][0]['elements'][0]['distance']['value']
            notificacao.tempo_estimado = google_data['rows'][0]['elements'][0]['duration']['text']
            notificacao.status = data['status']
            
            # Compromete a transação no banco de dados, seja atualizando a notificação existente ou criando uma nova.
            db.session.commit()

            # Retorna uma resposta com a distância atual e o tempo estimado.
            return notificacao, 200

        except Exception as e:
            return {'Erro ao manipular webhook': str(e)}, 500