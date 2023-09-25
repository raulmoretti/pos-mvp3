import requests
from flask import request
from project.models import Entrega
from project import db
from .google_api import google_matrix_api_request
from project.swagger import api_v1, model
from flask_restx import Resource

# Classe baseada na estrutura Flask RestPlus para a rotas relacionadas a "todas as entregas"
@api_v1.route('/entregas')
class EntregasResource(Resource):
    # Método GET para buscar todas as entregas
    def get(self):
        """
        Buscar todas as entregas
        """
        try:
            entregas = Entrega.query.all()
            entregas_lista = [entrega.to_dict() for entrega in entregas]
            return entregas_lista, 200
        except Exception as e:
            return {'message': 'Erro ao buscar entregas', 'error': str(e)}
        
    # Método POST para criar uma entrega
    @api_v1.expect(model)
    def post(self):
        """
        Criar uma entrega.
        Campos obrigatórios: email, remetente, destinatario, endereco_origem, endereco_destino, descricao, peso, cidade_origem, cidade_destino, cidade_atual

        Campos opcionais: status (default: 'Aguardando coleta')

        Campos não editáveis: tempo_estimado, distancia_atual

        Calcula o tempo_estimado e a distância_atual com base na cidade_origem e na cidade_destino diretamente pela Google Matrix API. 

        Como um novo pedido necessáriamente estará "Aguardando coleta", não é necessário criar uma notificação utilizando o webhook da notification_api.
        """
        try:
            data = request.get_json()

            # Verificando e removendo as chaves de campos "não editáveis" se existirem
            keys_to_remove = ['tempo_estimado', 'distancia_atual']
            for key in keys_to_remove:
                data.pop(key, None) 

            # Criando uma nova entrega
            nova_entrega = Entrega(**data)

            # Manda uma requisição para a API do Google Maps Matrix para atualizar a distância e o tempo estimado
            google_data = google_matrix_api_request(nova_entrega.cidade_origem, nova_entrega.cidade_destino)

            # Pega a resposta da requisição e atualiza os campos da entrega
            if google_data:
                nova_entrega.distancia_atual = google_data['rows'][0]['elements'][0]['distance']['value']
                nova_entrega.tempo_estimado = google_data['rows'][0]['elements'][0]['duration']['text']

            db.session.add(nova_entrega)
            db.session.commit()

            return {'message': 'Entrega criada'}, 201
        except Exception as e:
            return {'message': 'Erro ao criar entrega', 'error': str(e)}
    
# Classe baseada na estrutura Flask RestPlus para a rotas relacionadas a "uma entrega específica"
@api_v1.route('/entregas/<int:id>')
class EntregaResource(Resource):
    # Método GET para buscar uma entrega específica
    @api_v1.marshal_with(model)
    def get(self, id):
        """
        Buscar uma entrega específica pelo ID
        """
        try:
            entrega = Entrega.query.get(id)
            if entrega is None:
                return {'message': 'Entrega não encontrada'}, 404
            else:
                return entrega.to_dict(), 200
        except Exception as e:
            return {'message': 'Erro ao buscar entrega', 'error': str(e)}
    
    # Método PUT para atualizar uma entrega específica
    @api_v1.expect(model)
    def put(self, id):
        """
        Atualizar uma entrega específica pelo ID.
        Campos obrigatórios: email, remetente, destinatario, endereco_origem, endereco_destino, descricao, peso, cidade_origem, cidade_destino, cidade_atual

        Campos opcionais: status (default: 'Aguardando coleta')

        Campos não editáveis: tempo_estimado, distancia_atual

        Manda um pedido ao webhook da notification_api para atualizar a distância e o tempo estimado com base na cidade_atual e na cidade_destino, e para criar uma notificação com o status e a cidade_atual atualizados.

        Mnda um pedido ao notification_api para enviar um email com a atualização da entrega.
        """
        try:
            data = request.get_json()

            # Verificando e removendo as chaves de campos "não editáveis" se existirem
            keys_to_remove = ['tempo_estimado', 'distancia_atual']
            for key in keys_to_remove:
                data.pop(key, None) 

            entrega = Entrega.query.get(id)
            
            if not entrega:
                return {'message': 'Entrega não encontrada'}, 404

            if 'status' in data or 'cidade_atual' in data:
                # Mandar requisição ao notification_api para atualizar a notificação relacionada a entrega
                response = requests.post('http://notification_api:5000/api/v1/webhook', 
                    json={
                            "entrega_id": id, 
                            "status": data.get("status", entrega.status), 
                            "cidade_atual": data.get("cidade_atual", entrega.cidade_atual),
                            "cidade_destino": entrega.cidade_destino,
                            "email": entrega.email,
                            "destinatario": entrega.destinatario
                        })
                
                # Mandar requisição ao notification_api para enviar email com atualização sobre a entrega
                requests.get('http://notification_api:5000/api/v1/notificacao/{}'.format(id))

                if response.status_code != 200:
                    return {'message': 'Erro ao atualizar entrega', 'error': response.json()['message']}, 500

                entrega.distancia_atual = response.json()['distancia_atual']
                entrega.tempo_estimado = response.json()['tempo_estimado']

            for key, value in data.items():
                setattr(entrega, key, value)
            db.session.commit()
            return {'message': 'Entrega atualizada com sucesso'}, 200

        except Exception as e:
            return {'message': 'Erro ao atualizar entrega', 'error': str(e)}, 500

    # Método DELETE para deletar uma entrega específica
    def delete(self, id):
        """
        Deleta uma entrega específica pelo ID
        """
        try:
            entrega = Entrega.query.get(id)
            if not entrega:
                return {'message': 'Entrega não encontrada'}, 404
            else:
                # Manda um pedido ao notification_api para excluir a notificação relacionada a entrega
                requests.delete('http://notification_api:5000/api/v1/notificacao/{}'.format(id))

                db.session.delete(entrega)
                db.session.commit()
                return {'message': 'Entrega excluída com sucesso'}
        except Exception as e:
            return {'message': 'Erro ao excluir entrega', 'error': str(e)}, 500
        
# API no Swagger
api_v1.add_resource(EntregasResource, '/entregas')
api_v1.add_resource(EntregaResource, '/entregas/<int:id>')
        