# Representa valores de data e horário.
from datetime import datetime

# Recursos usados para validar os dados da API.
from pydantic import BaseModel, ConfigDict, Field


# Dados recebidos para criar um estudo.
class StudyCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=120,
    )

    description: str = Field(
        min_length=1,
    )


# Dados devolvidos pela API.
class StudyResponse(StudyCreate):
    # Permite converter um objeto SQLAlchemy em JSON.
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
