from sqlalchemy import Column, Integer, String
from src.infra.sqlalchemy.config.database import Base


class Serie(Base):
    __tablename__ = 'serie'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    ano = Column(Integer)
    genero = Column(String)
    qtd_temporadas = Column(Integer)
