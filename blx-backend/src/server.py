from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples, Usuario
from src.infra.sqlalchemy.config.database import get_db, criar_bd
from src.infra.sqlalchemy.repositorios.repositorio_produto \
    import RepositorioProduto
from src.infra.sqlalchemy.repositorios.repositorio_usuario \
    import RepositorioUsuario

# criar_bd()

app = FastAPI()

# CORS
origins = ['http://localhost:3000',
           'https://myapp.vercel.com']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

# Rotas PRODUTOS


@app.post('/produtos',
          status_code=status.HTTP_201_CREATED,
          response_model=ProdutoSimples)
def criar_produto(
        produto: Produto,
        db: Session = Depends(get_db)):
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado


@app.get('/produtos', response_model=List[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos


@app.put('/produtos/{id}', response_model=ProdutoSimples)
def atualizar_produto(
        id: int,
        produto: Produto,
        session: Session = Depends(get_db)):
    RepositorioProduto(session).editar(id, produto)
    produto.id = id
    return produto


@app.delete('/produtos/{id}')
def remover_produto(id: int, session: Session = Depends(get_db)):
    RepositorioProduto(session).remover(id)
    return


# USUARIOS
@app.post('/signup',
          status_code=status.HTTP_201_CREATED,
          response_model=Usuario)
def signup(usuario: Usuario, session: Session = Depends(get_db)):
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado


@app.get('/usuarios', response_model=List[Usuario])
def listar_usuario(session: Session = Depends(get_db)):
    usuarios = RepositorioUsuario(session).listar()
    return usuarios
