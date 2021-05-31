from fastapi.exceptions import HTTPException
from src.infra.sqlalchemy.repositorios.repositorio_usuario \
    import RepositorioUsuario
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from src.infra.sqlalchemy.config.database import get_db
from fastapi.security import OAuth2PasswordBearer, oauth2
from src.schemas.schemas import Usuario, UsuarioSimples, LoginData
from jose import JWTError, jwt
from datetime import datetime, timedelta

# JOSE Config vars
SECRET_KEY = 'chave-secreta'
ALGORITHM = 'HS256'
EXPIRES_IN_MINUTES = 30

router = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    dados = data.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MINUTES)

    dados.update({'exp': expiracao})

    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def obter_usuario_logado(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        telefone: str = payload.get('sub')
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')

    if not telefone:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')

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

    access_token = create_access_token(data={'sub': usuario.telefone})
    return {"access_token": access_token}


@router.get('/me')
def meus_dados(usuario_logado: Usuario = Depends(obter_usuario_logado)):
    return usuario_logado
