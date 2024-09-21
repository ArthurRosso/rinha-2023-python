import uuid
from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON

# SQLAlchemy setup
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apelido = Column(String, index=True, nullable=False)
    nome = Column(String, index=True, nullable=False)
    nascimento = Column(Date, nullable=False)
    stack = Column(JSON, nullable=True)

    # __table_args__ = (
    #     Index('ix_apelido_nome', "apelido", "nome"),  # Composite index for faster search
    # )