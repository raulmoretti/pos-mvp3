# Puxar imagem base oficial do python
FROM python:3.10.12-slim-buster

# Definir diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema operacional
RUN apt-get update && apt-get install -y netcat

# Instalar dependências
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Copiar projeto
COPY . /usr/src/app/

# Dar permissão de execução ao script de inicialização
RUN chmod +x /usr/src/app/entrypoint.sh

# Executar script de inicialização
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]