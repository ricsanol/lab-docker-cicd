# Importa o TestClient fornecido pelo FastAPI.
# Ele permite simular requisições HTTP sem precisar abrir o navegador
# e sem precisar iniciar manualmente o servidor Uvicorn.
from fastapi.testclient import TestClient

# Importa a aplicação FastAPI que criamos no arquivo app/main.py.
from app.main import app


# Cria um cliente de teste conectado à nossa aplicação.
# A variável client poderá executar requisições GET, POST e outros métodos.
client = TestClient(app)


# Toda função de teste deve começar com "test_".
# Dessa forma, o pytest consegue localizar e executar automaticamente o teste.
def test_home() -> None:
    # Simula uma requisição HTTP GET para a rota principal "/".
    response = client.get("/")

    # Verifica se o código HTTP retornado foi 200.
    # O código 200 significa que a requisição foi processada com sucesso.
    assert response.status_code == 200

    # Converte a resposta JSON para um dicionário Python
    # e verifica se o conteúdo retornado é exatamente o esperado.
    assert response.json() == {
        "status": "online",
        "message": "Laboratório Docker e CI/CD",
    }


# Cria um segundo teste para verificar a rota de saúde.
def test_health() -> None:
    # Simula uma requisição HTTP GET para "/health".
    response = client.get("/health")

    # Confirma que a API respondeu com sucesso.
    assert response.status_code == 200

    # Confirma que o conteúdo JSON possui o status esperado.
    assert response.json() == {
        "status": "healthy",
    }