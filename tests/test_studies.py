# Define o tipo da função que fornece sessões de teste.
from collections.abc import Generator

# Recursos utilizados para criar o banco temporário.
from sqlalchemy import delete, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

# Recursos da aplicação.
from fastapi.testclient import TestClient

from app.database import Base, get_session
from app.main import app
from app.models import Study

# Cria um banco SQLite temporário apenas para os testes.
test_engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


# Cria a tabela studies no banco temporário.
Base.metadata.create_all(bind=test_engine)


# Fornece uma sessão conectada ao banco de teste.
def override_get_session() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session


# Faz a API utilizar o banco temporário durante os testes.
app.dependency_overrides[get_session] = override_get_session


# Cria um cliente HTTP conectado à aplicação.
client = TestClient(app)


# Apaga registros criados por testes anteriores.
def clear_studies() -> None:
    with Session(test_engine) as session:
        session.execute(delete(Study))
        session.commit()


# Testa a criação de um registro.
def test_create_study() -> None:
    clear_studies()

    response = client.post(
        "/studies",
        json={
            "title": "Docker Compose",
            "description": "Integração com PostgreSQL",
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["title"] == "Docker Compose"
    assert response_data["description"] == "Integração com PostgreSQL"
    assert isinstance(response_data["id"], int)
    assert response_data["created_at"] is not None


# Testa a listagem dos registros.
def test_list_studies() -> None:
    clear_studies()

    client.post(
        "/studies",
        json={
            "title": "Persistência",
            "description": "Dados armazenados em volume Docker",
        },
    )

    response = client.get("/studies")

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 1
    assert response_data[0]["title"] == "Persistência"
    assert response_data[0]["description"] == ("Dados armazenados em volume Docker")

    # Testa a consulta de um registro específico.


def test_get_study() -> None:
    clear_studies()

    create_response = client.post(
        "/studies",
        json={
            "title": "PostgreSQL",
            "description": "Banco de dados do laboratório",
        },
    )

    study_id = create_response.json()["id"]

    response = client.get(f"/studies/{study_id}")

    assert response.status_code == 200
    assert response.json()["id"] == study_id
    assert response.json()["title"] == "PostgreSQL"


# Testa a consulta de um identificador inexistente.
def test_get_study_not_found() -> None:
    clear_studies()

    response = client.get("/studies/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Registro de estudo não encontrado.",
    }


# Testa a exclusão de um registro.
def test_delete_study() -> None:
    clear_studies()

    create_response = client.post(
        "/studies",
        json={
            "title": "Docker",
            "description": "Registro que será excluído",
        },
    )

    study_id = create_response.json()["id"]

    delete_response = client.delete(f"/studies/{study_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/studies/{study_id}")

    assert get_response.status_code == 404


# Testa a exclusão de um identificador inexistente.
def test_delete_study_not_found() -> None:
    clear_studies()

    response = client.delete("/studies/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Registro de estudo não encontrado.",
    }
