# Representa data e horário no Python.
from datetime import datetime

# Tipos de colunas e funções oferecidos pelo SQLAlchemy.
from sqlalchemy import DateTime, String, Text, func

# Recursos utilizados para mapear classes Python para tabelas.
from sqlalchemy.orm import Mapped, mapped_column

# Classe-base compartilhada por todos os modelos.
from app.database import Base


# Representa a tabela de registros de estudo.
class Study(Base):
    # Nome que a tabela terá dentro do PostgreSQL.
    __tablename__ = "studies"

    # Identificador numérico único gerado pelo PostgreSQL.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Título curto informado pelo usuário.
    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    # Descrição detalhada do conteúdo estudado.
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Data e horário em que o registro foi criado.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
