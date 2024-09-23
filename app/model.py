import uuid
from sqlalchemy import Column, String, Date, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy setup
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apelido = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    nascimento = Column(Date, nullable=False)
    stack = Column(String, nullable=True)

    __table_args__ = (
        Index('ix_busca', "apelido", "nome", "stack"),  # Composite index for faster search
    )