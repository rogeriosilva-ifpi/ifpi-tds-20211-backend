from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.schemas.schemas import LoginSucesso, Usuario, UsuarioSimples, LoginData
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_usuario \
    import RepositorioUsuario
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()


@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=UsuarioSimples)
def signup(usuario: Usuario, session: Session = Depends(get_db)):
    # verificar se já existe um para o telefone
    usuario_localizado = RepositorioUsuario(
        session).obter_por_telefone(usuario.telefone)

    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Já existe um usuário para este telefone')

    # criar novo usuario
    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado


@router.post('/token', response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha = login_data.senha
    telefone = login_data.telefone

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Telefone ou senha estão incorrentes!')

    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Telefone ou senha estão incorrentes!')
    # Gerar Token JWT
    token = token_provider.criar_access_token({'sub': usuario.telefone})
    return LoginSucesso(usuario=usuario, access_token=token)


@router.get('/me', response_model=UsuarioSimples)
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    return usuario
