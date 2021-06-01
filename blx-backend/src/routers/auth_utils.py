from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from jose import JWTError

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def obter_usuario_logado(token: str = Depends(oauth2_schema),
                         session: Session = Depends(get_db)):
    # decodificar o token, pegar o telefone, buscar usuario no bd e retornar
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')

    try:
        telefone = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception

    if not telefone:
        raise exception

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise exception

    return usuario
