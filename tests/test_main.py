# Importa o cliente de testes fornecido pelo FastAPI.
from fastapi.testclient import TestClient

# Importa a aplicação que será testada.
from app.main import app


# Cria um cliente que consegue fazer requisições para a API
# sem precisar iniciar o servidor Uvicorn.
client = TestClient(app)


# Testa o endpoint principal da aplicação.
def test_home() -> None:
    # Simula uma requisição HTTP GET para "/".
    response = client.get("/")

    # Confirma que a API respondeu com HTTP 200.
    assert response.status_code == 200

    # Confirma que o conteúdo retornado está correto.
    assert response.json() == {
        "status": "online",
        "message": "Laboratório Docker e CI/CD",
    }


# Testa o endpoint de verificação de saúde.
def test_health() -> None:
    # Simula uma requisição HTTP GET para "/health".
    response = client.get("/health")

    # Confirma que a API respondeu com HTTP 200.
    assert response.status_code == 200

    # Confirma que a aplicação informou estar saudável.
    assert response.json() == {
        "status": "healthy",
    }


# Testa o endpoint que informa a versão da aplicação.
def test_version() -> None:
    # Simula uma requisição HTTP GET para "/version".
    response = client.get("/version")

    # Confirma que a API respondeu com HTTP 200.
    assert response.status_code == 200

    # Confirma que a versão retornada é exatamente 1.2.0.
    assert response.json() == {
        "version": "1.2.0",
    }