# Define o tipo retornado pelo ciclo de vida da aplicação.
from collections.abc import AsyncIterator

# Permite executar ações na inicialização e no encerramento.
from contextlib import asynccontextmanager

# Permite criar um tipo que combina a sessão com a dependência do FastAPI.
from typing import Annotated

# Importa os recursos utilizados para criar a API.
from fastapi import Depends, FastAPI, HTTPException, Response, status

# Importa o recurso usado para construir consultas SQL.
from sqlalchemy import select

# Representa uma sessão de comunicação com o banco.
from sqlalchemy.orm import Session

# Importa a função que fornece sessões do PostgreSQL.
from app.database import Base, get_engine, get_session

# Importa o modelo que representa a tabela studies.
from app.models import Study

# Importa os contratos de entrada e saída da API.
from app.schemas import StudyCreate, StudyResponse

# Representa uma sessão fornecida automaticamente pelo FastAPI.
DatabaseSession = Annotated[Session, Depends(get_session)]


# Executa ações ao iniciar e encerrar a API.
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Cria somente as tabelas que ainda não existem.
    Base.metadata.create_all(bind=get_engine())

    # Mantém a aplicação funcionando.
    yield

    # Encerra o conjunto de conexões ao desligar.
    get_engine().dispose()


# Cria a aplicação FastAPI.
app = FastAPI(
    # Define o nome exibido na documentação automática.
    title="Laboratório Docker e CI/CD",
    # Define a versão atual da API.
    version="1.1.0",
    lifespan=lifespan,
)


# Responde às requisições GET feitas no endereço principal "/".
@app.get("/")
def home() -> dict[str, str]:
    # O FastAPI transforma este dicionário em uma resposta JSON.
    return {
        # Informa que a aplicação está online.
        "status": "online",
        # Mensagem apresentada para quem acessar a API.
        "message": "Laboratório Docker e CI/CD",
    }


# Responde às requisições GET feitas no endereço "/health".
@app.get("/health")
def health() -> dict[str, str]:
    # Informa que a aplicação está funcionando.
    return {
        "status": "healthy",
    }


# Responde às requisições GET feitas no endereço "/version".
@app.get("/version")
def version() -> dict[str, str]:
    # Retorna a versão atual da aplicação.
    return {
        "version": "1.1.0",
    }


# Cria e armazena um novo registro de estudo.
@app.post(
    "/studies",
    response_model=StudyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study(
    study_data: StudyCreate,
    session: DatabaseSession,
) -> StudyResponse:
    # Converte os dados recebidos em um objeto SQLAlchemy.
    study = Study(
        title=study_data.title,
        description=study_data.description,
    )

    # Prepara o objeto para ser inserido no PostgreSQL.
    session.add(study)

    # Confirma a inserção no banco.
    session.commit()

    # Atualiza o objeto com o ID e a data gerados pelo PostgreSQL.
    session.refresh(study)

    # Converte o objeto SQLAlchemy para o formato da resposta.
    return StudyResponse.model_validate(study)


# Consulta todos os registros de estudo.
@app.get(
    "/studies",
    response_model=list[StudyResponse],
)
def list_studies(
    session: DatabaseSession,
) -> list[StudyResponse]:
    # Cria uma consulta ordenada pelo identificador.
    statement = select(Study).order_by(Study.id)

    # Executa a consulta e obtém todos os registros.
    studies = session.scalars(statement).all()

    # Converte os objetos SQLAlchemy para respostas da API.
    return [StudyResponse.model_validate(study) for study in studies]


# Consulta um registro específico pelo identificador.
@app.get(
    "/studies/{study_id}",
    response_model=StudyResponse,
)
def get_study(
    study_id: int,
    session: DatabaseSession,
) -> StudyResponse:
    # Procura o registro pela chave primária.
    study = session.get(Study, study_id)

    # Retorna HTTP 404 quando o registro não existe.
    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estudo não encontrado.",
        )

    return StudyResponse.model_validate(study)


# Exclui um registro específico.
@app.delete(
    "/studies/{study_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_study(
    study_id: int,
    session: DatabaseSession,
) -> Response:
    # Procura o registro pela chave primária.
    study = session.get(Study, study_id)

    # Retorna HTTP 404 quando o registro não existe.
    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estudo não encontrado.",
        )

    # Marca o registro para exclusão.
    session.delete(study)

    # Confirma a exclusão no PostgreSQL.
    session.commit()

    # HTTP 204 indica sucesso sem conteúdo na resposta.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
