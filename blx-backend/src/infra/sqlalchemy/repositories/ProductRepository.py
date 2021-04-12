from sqlalchemy.orm import Session
from src.infra.sqlalchemy import schemas
from src.models import models


def criar(db: Session, produto: models.Produto):
    db_produto = schemas.Produto(nome=produto.nome,
                                 detalhes=produto.detalhes,
                                 preco=produto.preco,
                                 disponivel=produto.disponivel)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def listar(db: Session):
    produtos = db.query(schemas.Produto).all()
    return produtos
