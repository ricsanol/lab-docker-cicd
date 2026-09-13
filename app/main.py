# Importa a classe FastAPI da biblioteca fastapi.
# Essa classe será usada para criar a nossa aplicação web/API.
from fastapi import FastAPI

# Cria a aplicação FastAPI.
# A variável "app" representa nossa API.
app = FastAPI(
    # Define o nome que aparecerá na documentação automática.
    title="Laboratório Docker e CI/CD",
    # Define a versão atual da nossa API.
    version="1.1.0",
)


# O decorador @app.get("/") informa ao FastAPI que a função abaixo
# deverá ser executada quando alguém fizer uma requisição HTTP GET
# para o endereço principal "/" da aplicação.
#
# Exemplo:
# http://127.0.0.1:8000/
@app.get("/")
def home() -> dict[str, str]:
    # "def" cria uma função chamada home.
    #
    # -> dict[str, str] é uma indicação de tipo.
    # Ela informa que a função devolverá um dicionário:
    # - as chaves serão textos;
    # - os valores também serão textos.

    # O return devolve o resultado da função.
    # O FastAPI transforma automaticamente este dicionário Python
    # em uma resposta JSON.
    return {
        # Informa que a aplicação está online.
        "status": "online",
        # Mensagem apresentada para quem acessar a API.
        "message": "Laboratório Docker e CI/CD",
    }


# Cria uma segunda rota HTTP do tipo GET.
#
# Essa rota será utilizada para verificar a saúde da aplicação.
# Sistemas de monitoramento, Docker e servidores podem acessar
# esse endereço para verificar se a API está funcionando.
#
# Exemplo:
# http://127.0.0.1:8000/health
@app.get("/health")
def health() -> dict[str, str]:
    # Cria uma função chamada health.
    #
    # Ela também retorna um dicionário no formato:
    # texto como chave e texto como valor.

    # O FastAPI converterá este dicionário para JSON.
    return {
        # "healthy" indica que a aplicação está saudável.
        "status": "healthy",
    }


# O decorador informa que esta função responderá a requisições
# HTTP GET feitas no endereço /version.
@app.get("/version")
def version() -> dict[str, str]:
    # Retorna a versão atual da aplicação em formato JSON.
    # Esse tipo de endpoint ajuda a identificar qual versão está executando.
    return {"version": "1.1.0"}
