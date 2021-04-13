from src.infra.sqlalchemy.models import models
from src.schema import schemas
from .main import RepositorioBase


class RepositorioProduto(RepositorioBase):

    def criar(self, produto: schemas.Produto):
        db_produto = models.Produto(nome=produto.nome,
                                    detalhes=produto.detalhes,
                                    preco=produto.preco,
                                    disponivel=produto.disponivel)
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto

    def listar(self):
        produtos = self.db.query(models.Produto).all()
        return produtos
