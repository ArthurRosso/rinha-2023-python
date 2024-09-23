import uuid
import json
from fastapi.encoders import jsonable_encoder
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from model import Pessoa as db_pessoa
from schema import Pessoa as sc_pessoa
from schema import PessoaPayload as sc_pessoa_payload
from fastapi.responses import JSONResponse

from database import get_db_session

router = APIRouter()

@router.post("/pessoas", status_code=status.HTTP_201_CREATED)
async def criar_pessoa(
    pessoa_payload: sc_pessoa_payload,
    session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    # Verificar se já existe uma Pessoa com o mesmo nome ou apelido
    query = select(db_pessoa).where(
        (db_pessoa.apelido == pessoa_payload.apelido) |
        (db_pessoa.nome == pessoa_payload.nome)
    )
    result = await session.execute(query)
    existing_pessoa = result.scalars().first()

    # Se for encontrada uma duplicata, levantar um 422
    if existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Uma Pessoa com o mesmo apelido ou nome já exite"
        )
    
    pessoa_data = {
        "apelido": pessoa_payload.apelido,
        "nome": pessoa_payload.nome,
        "nascimento": pessoa_payload.nascimento,
        # Convert the stack list to a JSON string
        "stack": json.dumps(pessoa_payload.stack) if pessoa_payload.stack else None
    }

    print(pessoa_data)

    # Inserir a nova Pessoa na base de dados
    pessoa = db_pessoa(**pessoa_data)
    session.add(pessoa)
    await session.commit()
    await session.refresh(pessoa)

    return JSONResponse(
        content=jsonable_encoder(sc_pessoa.model_validate(pessoa)),
        status_code=status.HTTP_201_CREATED, 
        headers={"Location": f"/pessoas/{pessoa.id}"}
    )

@router.get("/pessoas/{id}", status_code=status.HTTP_200_OK)
async def consulta_pessoa(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> sc_pessoa:
    # Procurar uma Pessoa pelo ID
    pessoa = await session.get(db_pessoa, id)
    if pessoa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada",
        )
    return sc_pessoa.model_validate(pessoa)
    

@router.get("/pessoas", status_code=status.HTTP_200_OK)
async def busca_pessoa(
    t: Union[str, None] = None,
    session: AsyncSession = Depends(get_db_session),
) -> list[sc_pessoa]:
    if t is None:
        # pessoas = await session.scalars(select(db_pessoa))
        # return [sc_pessoa.model_validate(pessoa) for pessoa in pessoas]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informar o critério de busca é obrigatório"
        )
    
    query = select(db_pessoa).where(
        db_pessoa.apelido.contains(t) | db_pessoa.nome.contains(t) | db_pessoa.stack.contains(t)
    )
    
    result = await session.execute(query)
    
    pessoas = result.scalars().all()
    
    return [sc_pessoa.model_validate(pessoa) for pessoa in pessoas]


@router.get("/contagem-pessoas", status_code=status.HTTP_200_OK)
async def conta_pessoa(session: AsyncSession = Depends(get_db_session)) -> int:
    # Contar o número de pessoas na base de dados
    query = select(func.count()).select_from(db_pessoa)
    
    result = await session.execute(query)
    
    # Obter a contagem (devolve uma tupla, pelo que extraímos o primeiro elemento)
    return result.scalar_one()