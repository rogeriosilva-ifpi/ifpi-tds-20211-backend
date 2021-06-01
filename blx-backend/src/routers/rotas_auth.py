from fastapi.exceptions import HTTPException
from src.infra.sqlalchemy.repositorios.repositorio_usuario \
    import RepositorioUsuario
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import Usuario, UsuarioSimples, LoginData, LoginSucesso
from src.infra.providers import hash_provider, token_provider
from src.routers.router_utils import obter_usuario_logado


router = APIRouter()


@router.post('/signup',
             status_code=status.HTTP_201_CREATED, response_model=Usuario)
def signup(usuario: Usuario, session: Session = Depends(get_db)):
    usuario_encontrado = RepositorioUsuario(
        session).obter_por_telefone(usuario.telefone)

    if usuario_encontrado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Já existe um usuário com este telefone')

    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar(usuario)
    return usuario_criado


@router.post('/token', response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha = login_data.senha
    telefone = login_data.telefone

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(
            status_code=400, detail='Telefone e/ou senha errados!')

    if not hash_provider.verificar_hash(senha, usuario.senha):
        raise HTTPException(
            status_code=400, detail='Telefone e/ou senha errados!')

    access_token = token_provider.create_access_token(
        data={'sub': usuario.telefone})
    return {"usuario": usuario, "access_token": access_token}


@router.get('/me', response_model=UsuarioSimples)
def meus_dados(usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return usuario_logado
