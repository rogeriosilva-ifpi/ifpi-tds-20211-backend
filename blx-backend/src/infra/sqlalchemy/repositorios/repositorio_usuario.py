from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioUsuario():

    def __init__(self, session: Session):
        self.session = session

    def criar(self, usuario: schemas.Usuario):
        usuario_bd = models.Usuario(nome=usuario.nome,
                                    senha=usuario.senha,
                                    telefone=usuario.telefone)
        self.session.add(usuario_bd)
        self.session.commit()
        self.session.refresh(usuario_bd)
        return usuario_bd

    def listar(self):
        stmt = select(models.Usuario)
        usuarios = self.session.execute(stmt).scalars().all()
        return usuarios

    def obter_por_telefone_senha(self, telefone: str, senha: str):
        query = select(models.Usuario).where(
            and_(models.Usuario.telefone == telefone, models.Usuario.senha == senha))

        return self.session.execute(query).scalars().first()

    def obter_por_telefone(self, telefone: str):
        query = select(models.Usuario).where(
            models.Usuario.telefone == telefone)

        return self.session.execute(query).scalars().first()
