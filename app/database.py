# Permite acessar variáveis de ambiente.
import os

# Define o tipo usado por funções que entregam valores temporariamente.
from collections.abc import Generator

# Mantém apenas um mecanismo de conexão durante a execução da aplicação.
from functools import lru_cache

# Recursos utilizados para conectar e executar comandos no banco.
from sqlalchemy import Engine, create_engine, text

# Recursos utilizados pelos modelos e sessões.
from sqlalchemy.orm import DeclarativeBase, Session


# Obtém o endereço do PostgreSQL configurado no ambiente.
def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    # Produz uma mensagem clara caso a variável não esteja configurada.
    if database_url is None:
        raise RuntimeError("A variável DATABASE_URL não foi configurada.")

    return database_url


# O cache faz a aplicação reutilizar o mesmo mecanismo de conexão.
@lru_cache
def get_engine() -> Engine:
    return create_engine(
        get_database_url(),
        # Verifica uma conexão antes de reutilizá-la.
        pool_pre_ping=True,
    )


# Classe-base que será utilizada pelos modelos das tabelas.
class Base(DeclarativeBase):
    pass


# Disponibiliza uma sessão de banco para uma operação da API.
def get_session() -> Generator[Session, None, None]:
    # A sessão será encerrada automaticamente.
    with Session(get_engine()) as session:
        yield session


# Executa uma consulta simples para testar a comunicação.
def check_database_connection() -> bool:
    with get_engine().connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar_one() == 1
