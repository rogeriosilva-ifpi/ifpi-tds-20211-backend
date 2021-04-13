from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import SessionLocal, engine, get_db, criar_bd
from src.infra.sqlalchemy.models import models
from src.schema import schemas
from src.infra.sqlalchemy.repositorios.RepositorioProduto import RepositorioProduto
from fastapi import FastAPI, Depends
from typing import List

# Criar banco de dados
criar_bd()

app = FastAPI()


@app.post('/produtos', response_model=schemas.Produto)
def criar_produto(produto: schemas.Produto, db: Session = Depends(get_db)):
    return RepositorioProduto(db).criar(produto)


@app.get('/produtos', response_model=List[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return RepositorioProduto(db).listar()
