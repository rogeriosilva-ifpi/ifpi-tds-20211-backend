from sqlalchemy.orm import Session
from src.infra.sqlalchemy.database import SessionLocal, engine
from src.infra.sqlalchemy import schemas
from src.models import models
from src.infra.sqlalchemy.repositories import ProductRepository
from fastapi import FastAPI, Depends
from typing import List

# Criar banco de dados
schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/produtos', response_model=models.Produto)
def criar_produto(produto: models.Produto, db: Session = Depends(get_db)):
    return ProductRepository.criar(db, produto)


@app.get('/produtos', response_model=List[models.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return ProductRepository.listar(db)
