# Servidor

## Setup

Ferramentas necessárias para a inicialização deste projeto:

- Python
- Docker e Docker-Compose

## Passo a passo para a inicialização

- Clonar projeto;
- Entrar no diretório raíz do projeto, através de uma Interface de Linha de Comandos (CLI);
- Executar os comandos:
  - pip install -r requirements.txt
  - docker-compose up -d
- O seguinte comando inicializa o servidor principal:
  - uvicorn main:app
- Em seguida, deve-se entrar no diretório src/rabbitmq através de outra CLI e executar o seguinte comando, para inicializar o servidor consumidor das filas criadas através do RabbitMQ (Esse servidor ficará executando em foreground, portanto, é necessário ser uma CLI diferente da utilizada para inicializar o servidor principal da aplicação):
  - python consumer-server.py
