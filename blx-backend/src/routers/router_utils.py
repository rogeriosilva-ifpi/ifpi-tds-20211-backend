from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from src.infra.providers import token_provider
from src.infra.sqlalchemy.repositorios.repositorio_usuario \
    import RepositorioUsuario
from src.infra.sqlalchemy.config.database import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def obter_usuario_logado(token: str = Depends(oauth2_schema),
                         session: Session = Depends(get_db)):
    try:
        telefone: str = token_provider.verificar_access_token(token)
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
