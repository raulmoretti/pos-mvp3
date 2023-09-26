# Serviços de entrega e rastreamento de entrega
Este projeto consiste em duas APIs REST que operam em uma arquitetura de microserviços. Elas utilizam das APIs do Google Maps (Google Matrix API) e do Mailjet para envio de e-mails.

## Execução
Para sua execução é necessário:
1. Instale o Python3, PostgreSQL e Docker.
2. Criação de um arquivo .env.dev na pasta raiz do projeto, contendo os seguintes dados:
```sh
FLASK_APP=project/__init__.py
FLASK_DEBUG=1
DATABASE_URL_DELIVERY_API=postgresql://usuario:senha@db_delivery:5432/db_entregas
DATABASE_URL_NOTIFICATIONS_API=postgresql://usuario:senha@db_notification:5432/db_notificacoes
DELIVERY_API_URL=http://localhost:5001/entregas
NOTIFICATIONS_API_URL=http://localhost:5002/webhook
SQL_HOST_DELIVERY=db_delivery
SQL_HOST_NOTIFICATION=db_notification
SQL_PORT=5432
DATABASE=postgres
YOUR_API_KEY=SuaApiKeyDaGoogleMaps
MAILJET_API_KEY=SuaApiKeyDaMailjet
MAILJET_SECRET_KEY=SuaSecretKeyDaMailjet
MAILJET_SENDER_EMAIL=EmailDaPessoaQueEnvia
MAILJET_SENDER_NAME=NomeDaPessoaQueEnvia
```
3. Abra o terminal na raiz do projeto e digite o seguinte comando:
```sh
docker-compose up --build
```
