import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class Pessoa(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    apelido: str
    nome: str
    nascimento: date
    stack: Optional[list[str]]

class PessoaPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    apelido: str = Field(min_length=1, max_length=32)
    nome: str = Field(min_length=1, max_length=100)
    nascimento: date
    stack: Optional[list[str]]