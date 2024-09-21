from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Request, HTTPException
from fastapi.exceptions import RequestValidationError

from database import migrate_tables
import pessoa

@asynccontextmanager
async def lifespan(app: FastAPI):
    await migrate_tables()
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)

app.include_router(pessoa.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if error['input'] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nome, apelido ou nascimento não podem ser nulos"
            )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Nome, apelido, nascimento ou stack devem ter os tipos corretos"
    )


@app.get("/")
async def read_root():
    return {"Hello": "World"}
