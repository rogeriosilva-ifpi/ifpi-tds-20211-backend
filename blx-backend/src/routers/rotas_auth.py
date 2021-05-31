from fastapi.exceptions import HTTPException
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from src.infra.sqlalchemy.config.database import get_db
from fastapi.security import OAuth2PasswordBearer, oauth2
from src.schemas.schemas import Usuario, UsuarioSimples, LoginData

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def decodificar_token(token):
    return UsuarioSimples(nome='Rogério', telefone='(86) 99459-3247')


def obter_usuario_logado(token: str = Depends(oauth2_schema)):
    usuario = decodificar_token(token)
    return usuario


@router.post('/token')
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha_hash = login_data.senha
    telefone = login_data.telefone
    usuario: Usuario = RepositorioUsuario(session).obter_por_telefone_senha(
        telefone, senha_hash)

    if not usuario:
        raise HTTPException(
            status_code=400, detail='Telefone e/ou senha errados!')

    return {"access_token": usuario.telefone}


@router.get('/me')
def meus_dados(usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return usuario_logado
