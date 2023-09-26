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
MAILJET_SENDER_EMAIL=emaildapessoaqueenvia@email.com
MAILJET_SENDER_NAME=NomeDaPessoaQueEnvia
```
3. Abra o terminal na raiz do projeto e digite o seguinte comando:
```sh
docker-compose up --build
```
O comando acima, inserido no terminal da raiz do projeto, instrui o Docker Compose a construir e iniciar o aplicativo Docker. O flag `--build` garante a construção das imagens antes de iniciar os contêineres, ideal para quando se incia a aplicação pela primeira vez ou após alterações computacionais. Utilizando as diretivas do arquivo `docker-compose.yml` localizado na raiz do projeto, o Docker Compose se encarrega de construir a aplicação e iniciar todos os serviços requeridos para rodar a mesma, como banco de dados e servidor web. Após completa execução, a aplicação será acessível na porta indicada no arquivo Docker Compose.

4. Documentação pode ser encontrada em:
- API de Entregas: http://localhost:5001/swagger
- API de Notificações: http://localhost:5002/swagger

Para o teste das APIs pode ser utilizado softwares como Postman e Insomnia.
